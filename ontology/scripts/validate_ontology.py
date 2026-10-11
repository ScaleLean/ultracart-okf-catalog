#!/usr/bin/env python3
"""Validate the UltraCart Store Ontology.

  --offline            selected-dataset historical schema checks (no BigQuery/auth);
                       semantic types, scope and key uniqueness remain unverified
  --compiled CONFIG    compile with CONFIG, then bq dry-run every statement (needs auth)

Exit 0 = pass.
"""
import argparse
import pathlib
import re
import subprocess
import sys

import yaml
from offline_contract import check_binding, DATASETS

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT.parent / "concepts" / "tables_by_name"
failures, warnings = [], []
CHECK_CONFIG = {"dataset": DATASETS}


def fail(msg):
    failures.append(msg)
    print(f"FAIL  {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"warn  {msg}")


def ok(msg):
    print(f"ok    {msg}")


def front_matter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
    if not m:
        fail(f"{path.relative_to(ROOT)}: no frontmatter")
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        fail(f"{path.relative_to(ROOT)}: YAML error: {e}")
        return None


def check_object(meta, path, all_objects):
    name = meta.get("object")
    rel = path.relative_to(ROOT)
    for req in ("object", "domain", "tier", "resource", "version", "grain", "key", "source", "properties", "pii"):
        if req not in meta:
            fail(f"{rel}: missing '{req}'")
            return
    for error in check_binding(meta, CHECK_CONFIG, ROOT.parent):
        fail(f"{rel}: {error}")
    for link in meta.get("links", []) or []:
        if link["to"] not in all_objects:
            fail(f"{rel}: link target '{link['to']}' is not a defined object")
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--compiled")
    ap.add_argument("--config", help="Offline selected dataset bindings; no live access.")
    args = ap.parse_args()
    global CHECK_CONFIG
    if args.config:
        CHECK_CONFIG = yaml.safe_load(pathlib.Path(args.config).read_text())
    if args.offline and args.compiled:
        ap.error("--offline cannot be combined with --compiled")

    object_files = sorted(ROOT.glob("objects/**/*.md"))
    metas = {}
    urns = {}
    for f in object_files:
        meta = front_matter(f)
        if not meta or meta.get("type") != "Ontology Object":
            continue
        metas[meta["object"]] = (meta, f)
        urn = meta.get("resource", "")
        if urn in urns:
            fail(f"duplicate URN {urn} ({f.name} and {urns[urn]})")
        urns[urn] = f.name

    sys.path.insert(0, str(ROOT.parent / 'scripts'))
    from build_knowledge_manifest import check_outputs, dependencies
    from audit_agent_usability import has_wildcard_projection
    def_files = sorted(ROOT.glob("definitions/*.md"))
    def_names = set()
    for f in def_files:
        meta = front_matter(f)
        if meta and meta.get("type") == "Ontology Definition":
            def_names.add(meta["definition"])

    families = set((front_matter(ROOT / 'identity/identity_spine.md') or {}).get('families', []))
    for name, (meta, _) in metas.items():
        if meta.get('key', {}).get('identity_family') not in families:
            fail(f"{name}: unknown identity family")

    # link targets may be objects OR named definitions (both compile to views)
    for name, (meta, f) in metas.items():
        check_object(meta, f, set(metas) | def_names)
    ok(f"{len(metas)} objects checked against dataset-specific historical schemas (structural only; scope/grain and derived types unverified)")
    n_defs = 0
    for f in def_files:
        meta = front_matter(f)
        if not meta or meta.get("type") != "Ontology Definition":
            continue
        n_defs += 1
        rel = f.relative_to(ROOT)
        for req in ("definition", "resource", "version", "sql", "summary"):
            if req not in meta:
                fail(f"{rel}: missing '{req}'")
        sql = meta.get("sql", "")
        if has_wildcard_projection(sql):
            fail(f"{rel}: wildcard projection forbidden")
        try:
            check_outputs(meta)
        except ValueError as e:
            fail(f"{rel}: {e}")
        try:
            refs = dependencies(meta)
        except ValueError as e:
            fail(f"{rel}: {e}")
            refs = []
        for obj_ref in refs:
            if obj_ref not in metas and not any(
                d2 != f and (front_matter(d2) or {}).get("definition") == obj_ref for d2 in def_files
            ):
                fail(f"{rel}: sql references {{{{ontology}}}}.{obj_ref} — not a defined object/definition")
        for p in re.findall(r"\{\{param\.(\w+)\}\}", sql):
            declared = meta.get("parameters") or {}
            names = {x["name"] for x in declared} if isinstance(declared, list) else set(declared)
            if p not in names:
                fail(f"{rel}: sql uses param '{p}' not declared in parameters")
    ok(f"{n_defs} named definitions checked")

    n_actions = 0
    for f in sorted(ROOT.glob("actions/**/*.md")):
        if f.name == "README.md":
            continue
        meta = front_matter(f)
        if not meta or meta.get("type") != "Ontology Action":
            continue
        n_actions += 1
        for req in ("action", "family", "object", "resource", "api", "mutates", "risk", "required_guards", "status"):
            if req not in meta:
                fail(f"{f.relative_to(ROOT)}: missing '{req}'")
        if meta.get("object") not in metas:
            fail(f"{f.relative_to(ROOT)}: action object '{meta.get('object')}' not a defined object")
    ok(f"{n_actions} actions checked")

    ledger = ROOT / "links" / "coverage_ledger.md"
    if ledger.exists():
        ledger_text = ledger.read_text()
        catalog_tables = {p.stem for p in CATALOG.glob("*.md")} - {"index"}
        missing = {t for t in catalog_tables if f"`{t}`" not in ledger_text}
        if missing:
            fail(f"coverage_ledger missing {len(missing)} tables: {sorted(missing)[:8]}{'…' if len(missing) > 8 else ''}")
        else:
            ok(f"coverage ledger covers all {len(catalog_tables)} canonical tables")
    else:
        fail("links/coverage_ledger.md does not exist")

    if args.compiled:
        cfg_path = args.compiled
        res = subprocess.run([sys.executable, str(ROOT / "scripts" / "compile_ontology.py"),
                              "--config", cfg_path], capture_output=True, text=True)
        if res.returncode != 0:
            fail(f"compile failed: {res.stderr.strip()[:300]}")
        else:
            ok(res.stdout.strip())
            cfg = yaml.safe_load(pathlib.Path(cfg_path).read_text())
            sql_file = ROOT / "build" / cfg["merchant_id"] / "ontology_views.sql"
            for stmt in [s.strip() for s in sql_file.read_text().split(";") if s.strip() and not s.strip().startswith("--")]:
                label = (re.search(r"VIEW `[^`]+\.(\w+)`", stmt) or re.search(r"SCHEMA", stmt)) and \
                        (re.search(r"VIEW `[^`]+\.(\w+)`", stmt).group(1) if "VIEW" in stmt else "schema")
                if "CREATE SCHEMA" in stmt:
                    continue  # dry-run of schema DDL is a no-op decision; views are the test
                body = stmt.split(" AS\n", 1)[1] if " AS\n" in stmt else None
                if body is None:
                    continue
                r = subprocess.run(["bq", "query", f"--project_id={cfg['billing_project']}",
                                    "--use_legacy_sql=false", "--dry_run", body],
                                   capture_output=True, text=True, timeout=120)
                if r.returncode != 0:
                    fail(f"dry-run {label}: {(r.stderr or r.stdout).strip().splitlines()[-1][:200]}")
                else:
                    ok(f"dry-run {label}")

    print(f"\n{'PASS' if not failures else 'FAIL'} — {len(failures)} failure(s), {len(warnings)} warning(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
