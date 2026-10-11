#!/usr/bin/env python3
"""Generate unverified local ontology review previews; no live queries or deployment.

Ordinary compilation is refused because offline metadata cannot establish scope,
grain uniqueness or derived SQL semantics. Use --offline-preview --config CONFIG
[--out SCRATCH | --stdout] only for local review. Private overlays stay private.

Selected dataset fields/direct types, config identifiers/parameter types and
available dependencies are checked. Unsupported binding overrides fail closed.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys

import yaml
from offline_contract import check_binding, binding_parts
from sql_syntax import rewrite_ontology_references

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_front_matter(path: pathlib.Path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path}: no YAML frontmatter")
    return yaml.safe_load(m.group(1))


def subst(template: str, cfg: dict, *, replace_ontology=True) -> str:
    out = template
    out = out.replace("{{source_project}}", cfg["source_project"])
    out = out.replace("{{merchant_id}}", cfg["merchant_id"])
    for tier, name in cfg.get("dataset", {}).items():
        out = out.replace("{{dataset.%s}}" % tier, name)
    if replace_ontology:
        out = out.replace("{{ontology}}", f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}')
    return out


def compile_object(meta: dict, cfg: dict, *, offline_preview=False) -> str:
    obj = meta["object"]
    if cfg.get("bindings"):
        raise ValueError("binding overrides unsupported offline: cannot establish scope/grain")
    if not offline_preview:
        raise ValueError("offline evidence cannot establish scope, grain uniqueness or semantic types; deployable compilation refused")
    errors = check_binding(meta, cfg, ROOT.parent)
    if errors:
        raise ValueError(f"{obj}: " + "; ".join(errors))
    validate_config(cfg)
    table = subst(meta["source"]["default_table"], cfg)
    cols = []
    for p in meta["properties"]:
        src = p["source"]
        expr = src if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", src) else f"({src})"
        cols.append(f"  {expr} AS {p['name']}" if expr != p["name"] else f"  {p['name']}")
    where = ""
    mf = meta["source"].get("merchant_filter")
    if mf:
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
    validate_config(cfg)
    sql = meta["sql"]
    for k, v in params.items():
        sql = sql.replace("{{param.%s}}" % k, str(v).lower() if isinstance(v, bool) else str(v))
    onto = f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}'
    sql = rewrite_ontology_references(sql, onto)
    sql = subst(sql, cfg, replace_ontology=False)
    name = meta["definition"]
    desc = f"NAMED DEFINITION v{meta['version']}: {meta.get('summary', '')} | urn={meta['resource']} | params={params}"
    view = f"{cfg['ontology_project']}.{cfg['ontology_dataset']}.{name}"
    return (
        f"CREATE OR REPLACE VIEW `{view}`\n"
        f"OPTIONS (description = {json.dumps(desc)}) AS\n{sql.strip().rstrip(';')};"
    )


def validate_config(cfg):
    if cfg.get('bindings'):
        raise ValueError('binding overrides unsupported offline: cannot establish scope/grain')
    for key in ('source_project', 'ontology_project', 'ontology_dataset', 'merchant_id'):
        if not isinstance(cfg.get(key), str) or not re.fullmatch(r'[A-Za-z0-9_-]+', cfg[key]):
            raise ValueError(f'invalid or missing identifier: {key}')
    for key, value in (cfg.get('parameters') or {}).items():
        if key not in {'include_channel_partner_orders', 'repeat_min_orders', 'lapsed_window_days'}:
            raise ValueError(f'unsupported parameter {key}')
        if key == 'include_channel_partner_orders':
            if type(value) is not bool:
                raise ValueError(f'{key} requires BOOLEAN')
        elif type(value) is not int or value < 1:
            raise ValueError(f'{key} requires positive INTEGER')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--offline-preview", action="store_true", help="Emit unverified local review SQL only; never deployment approval.")
    ap.add_argument("--out", type=pathlib.Path, help="Local scratch output directory for offline preview.")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(pathlib.Path(args.config).read_text())

    if not args.offline_preview:
        raise SystemExit("offline evidence cannot establish scope, grain uniqueness or semantic types; deployable compilation refused")
    validate_config(cfg)
    exclude = set(cfg.get("exclude_objects", []) or [])
    statements = [
        f"CREATE SCHEMA IF NOT EXISTS `{cfg['ontology_project']}.{cfg['ontology_dataset']}`\n"
        f"OPTIONS (location = 'US', description = 'UltraCart Store Ontology (compiled; do not hand-edit). Spec: ontology/SPEC.md');"
    ]
    # Import lazily: sidecar construction shares this module's frontmatter loader.
    sys.path.insert(0, str(ROOT.parent / 'scripts'))
    from build_knowledge_manifest import build_manifest, dependencies
    knowledge = build_manifest(ROOT.parent)
    manifest = {key: knowledge[key] for key in ('manifest_version', 'okf_version', 'ontology_version',
                'generated_at', 'source_captured_at', 'verified_at', 'historical_evidence',
                'source_commit', 'source_hashes', 'trust', 'validation_limits')}
    manifest.update({"merchant_id": cfg["merchant_id"], "deployable": False, "objects": {}, "definitions": {}})
    known_objects = {load_front_matter(f)['object'] for f in ROOT.glob('objects/**/*.md')}
    if exclude - known_objects:
        raise ValueError(f'unknown excluded objects: {sorted(exclude - known_objects)}')

    object_files = sorted(ROOT.glob("objects/**/*.md"))
    # dependency-light ordering: objects first (alphabetical is fine — objects only
    # reference source tables), then definitions (which reference objects).
    for f in object_files:
        meta = load_front_matter(f)
        if meta.get("type") != "Ontology Object" or meta["object"] in exclude:
            continue
        statements.append(compile_object(meta, cfg, offline_preview=True))
        dataset, table_name = binding_parts(meta, cfg)
        schema_path = f'tables/{dataset}/{table_name}.md'
        manifest['source_hashes'][schema_path] = hashlib.sha256((ROOT.parent / schema_path).read_bytes()).hexdigest()
        manifest["objects"][meta["object"]] = {
            "view": f'{cfg["ontology_project"]}.{cfg["ontology_dataset"]}.{meta["object"]}',
            "binding": subst(meta["source"]["default_table"], cfg),
            "version": meta["version"],
            "properties": [p["name"] for p in meta["properties"]],
            "output_types": {p["name"]: p["type"] for p in meta["properties"]},
            "dependencies": [subst(meta["source"]["default_table"], cfg)],
            "scope_state": knowledge['objects'][meta['object']]['scope_state'],
            "grain_state": 'declared_uniqueness_unverified',
            "output_type_state": 'direct_checked_derived_declared',
            "schema_evidence": schema_path,
        }

    # definitions may reference other definitions — topological order by {{ontology}}.X refs
    def_metas = []
    for f in sorted(ROOT.glob("definitions/*.md")):
        meta = load_front_matter(f)
        if meta.get("type") == "Ontology Definition":
            def_metas.append(meta)
    def_names = {m["definition"] for m in def_metas}
    for meta in def_metas:
        missing = set(dependencies(meta)) - (set(manifest['objects']) | def_names)
        if missing:
            raise ValueError(f"{meta['definition']}: unavailable dependency {sorted(missing)}")
    deps = {
        m["definition"]: set(dependencies(m)) & def_names
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
        manifest["definitions"][meta["definition"]] = knowledge["definitions"][meta["definition"]]

    sql_out = (
        "-- UNVERIFIED OFFLINE REVIEW PREVIEW — NOT FOR DEPLOYMENT.\n"
        f"-- merchant: {cfg['merchant_id']} | spec: ontology/SPEC.md\n\n"
        + "\n\n".join(statements) + "\n"
    )
    if args.stdout:
        print(sql_out)
        return
    out_dir = args.out or ROOT / "build" / cfg["merchant_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ontology_views.sql").write_text(sql_out)
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"compiled {len(manifest['objects'])} objects + {len(manifest['definitions'])} definitions -> {out_dir}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as e:
        raise SystemExit(str(e))
