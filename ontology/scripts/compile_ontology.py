#!/usr/bin/env python3
"""Compile the merchant-neutral UltraCart Store Ontology into merchant-specific BigQuery DDL.

Usage:
  python3 scripts/compile_ontology.py --config config/local/<merchant>.yml [--stdout]

Reads every objects/**/*.md and definitions/*.md, substitutes the merchant config,
and emits:
  build/<merchant_id>/ontology_views.sql   (CREATE SCHEMA + CREATE OR REPLACE VIEW ...)
  build/<merchant_id>/manifest.json        (object -> view -> source binding + property list)

Design rules enforced here (see SPEC.md):
  - SQL is generated only; property `source` expressions are the single source of truth.
  - Binding overrides change WHERE data comes from, never the property contract.
  - Definitions compile over ontology objects (they reference {{ontology}}.<object>).
"""
import argparse
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_front_matter(path: pathlib.Path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path}: no YAML frontmatter")
    return yaml.safe_load(m.group(1))


def subst(template: str, cfg: dict) -> str:
    out = template
    out = out.replace("{{source_project}}", cfg["source_project"])
    out = out.replace("{{merchant_id}}", cfg["merchant_id"])
    for tier, name in cfg.get("dataset", {}).items():
        out = out.replace("{{dataset.%s}}" % tier, name)
    out = out.replace("{{ontology}}", f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}')
    return out


def compile_object(meta: dict, cfg: dict) -> str:
    obj = meta["object"]
    binding_override = cfg.get("bindings", {}).get(obj)
    table = binding_override or subst(meta["source"]["default_table"], cfg)
    cols = []
    for p in meta["properties"]:
        src = p["source"]
        expr = src if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", src) else f"({src})"
        cols.append(f"  {expr} AS {p['name']}" if expr != p["name"] else f"  {p['name']}")
    where = ""
    mf = meta["source"].get("merchant_filter")
    if mf and not binding_override:
        where = f"\nWHERE {subst(mf, cfg)}"
    unnest = meta["source"].get("unnest")
    from_clause = f"`{table}`"
    if unnest:
        from_clause += f", UNNEST({unnest['field']}) AS {unnest['alias']}"
    desc = f"{meta['grain']} | urn={meta['resource']} | v{meta['version']} | compiled from OKF ontology"
    view = f"{cfg['ontology_project']}.{cfg['ontology_dataset']}.{obj}"
    return (
        f"CREATE OR REPLACE VIEW `{view}`\n"
        f"OPTIONS (description = {json.dumps(desc)}) AS\n"
        f"SELECT\n" + ",\n".join(cols) + f"\nFROM {from_clause}{where};"
    )


def compile_definition(meta: dict, cfg: dict) -> str:
    # parameters may be given as {name: default} or list of {name, default, meaning}
    raw_params = meta.get("parameters") or {}
    if isinstance(raw_params, list):
        params = {p["name"]: p["default"] for p in raw_params}
    else:
        params = dict(raw_params)
    params.update(cfg.get("parameters", {}) or {})
    sql = meta["sql"]
    for k, v in params.items():
        sql = sql.replace("{{param.%s}}" % k, str(v))
    sql = subst(sql, cfg)
    # normalize ontology-view references to fully-backticked form regardless of
    # whether the author backticked `{{ontology}}.x`, {{ontology}}.x, or partially
    onto = f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}'
    sql = re.sub(r"`?" + re.escape(onto) + r"`?\.`?(\w+)`?", rf"`{onto}.\1`", sql)
    name = meta["definition"]
    desc = f"NAMED DEFINITION v{meta['version']}: {meta.get('summary', '')} | urn={meta['resource']} | params={params}"
    view = f"{cfg['ontology_project']}.{cfg['ontology_dataset']}.{name}"
    return (
        f"CREATE OR REPLACE VIEW `{view}`\n"
        f"OPTIONS (description = {json.dumps(desc)}) AS\n{sql.strip().rstrip(';')};"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(pathlib.Path(args.config).read_text())

    exclude = set(cfg.get("exclude_objects", []) or [])
    statements = [
        f"CREATE SCHEMA IF NOT EXISTS `{cfg['ontology_project']}.{cfg['ontology_dataset']}`\n"
        f"OPTIONS (location = 'US', description = 'UltraCart Store Ontology (compiled; do not hand-edit). Spec: ontology/SPEC.md');"
    ]
    manifest = {"merchant_id": cfg["merchant_id"], "objects": {}, "definitions": {}}

    object_files = sorted(ROOT.glob("objects/**/*.md"))
    # dependency-light ordering: objects first (alphabetical is fine — objects only
    # reference source tables), then definitions (which reference objects).
    for f in object_files:
        meta = load_front_matter(f)
        if meta.get("type") != "Ontology Object" or meta["object"] in exclude:
            continue
        statements.append(compile_object(meta, cfg))
        manifest["objects"][meta["object"]] = {
            "view": f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}.{meta["object"]}',
            "binding": cfg.get("bindings", {}).get(meta["object"])
            or subst(meta["source"]["default_table"], cfg),
            "version": meta["version"],
            "properties": [p["name"] for p in meta["properties"]],
        }

    # definitions may reference other definitions — topological order by {{ontology}}.X refs
    def_metas = []
    for f in sorted(ROOT.glob("definitions/*.md")):
        meta = load_front_matter(f)
        if meta.get("type") == "Ontology Definition":
            def_metas.append(meta)
    def_names = {m["definition"] for m in def_metas}
    deps = {
        m["definition"]: {r for r in re.findall(r"\{\{ontology\}\}\.(\w+)", m["sql"]) if r in def_names}
        for m in def_metas
    }
    ordered, placed = [], set()
    while def_metas:
        progressed = False
        for m in list(def_metas):
            if deps[m["definition"]] <= placed:
                ordered.append(m)
                placed.add(m["definition"])
                def_metas.remove(m)
                progressed = True
        if not progressed:
            raise SystemExit(f"circular definition dependency among: {[m['definition'] for m in def_metas]}")
    for meta in ordered:
        statements.append(compile_definition(meta, cfg))
        manifest["definitions"][meta["definition"]] = {"version": meta["version"]}

    sql_out = (
        "-- Compiled UltraCart Store Ontology — DO NOT HAND-EDIT.\n"
        f"-- merchant: {cfg['merchant_id']} | spec: ontology/SPEC.md\n\n"
        + "\n\n".join(statements) + "\n"
    )
    if args.stdout:
        print(sql_out)
        return
    out_dir = ROOT / "build" / cfg["merchant_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ontology_views.sql").write_text(sql_out)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"compiled {len(manifest['objects'])} objects + {len(manifest['definitions'])} definitions -> {out_dir}")


if __name__ == "__main__":
    main()
