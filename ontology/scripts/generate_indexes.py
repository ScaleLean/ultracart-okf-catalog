#!/usr/bin/env python3
"""Generate links/link_graph.md and links/coverage_ledger.md from the ontology sources.

  python3 scripts/generate_indexes.py [--domain-map PATH]

- link_graph.md is fully derived from object frontmatter (regenerate any time).
- coverage_ledger.md: every canonical OKF table -> its ontology role. Table meanings,
  domains and tiers are seeded from the domain map on first generation and then live
  in this repo; the ledger is regenerated from objects + the previous ledger (or the
  domain map when provided).
"""
import argparse
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT.parent / "concepts" / "tables_by_name"


def front_matter(path):
    m = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None


def load_objects():
    objs = {}
    for f in sorted(ROOT.glob("objects/**/*.md")):
        meta = front_matter(f)
        if meta and meta.get("type") == "Ontology Object":
            objs[meta["object"]] = meta
    return objs


def parse_domain_map(path):
    """table -> (domain, tier, meaning) from the overnight domain map."""
    info = {}
    if not path or not pathlib.Path(path).exists():
        return info
    text = pathlib.Path(path).read_text()
    for m in re.finditer(
        r"^### (\w+)\s+\[domain: ([\w_]+)\]\s+\[tier: (\w+)\]\n- meaning: ([^\n]+)",
        text, re.MULTILINE,
    ):
        info[m.group(1)] = (m.group(2), m.group(3), m.group(4).strip())
    return info


def parse_existing_ledger():
    info = {}
    ledger = ROOT / "links" / "coverage_ledger.md"
    if not ledger.exists():
        return info
    for m in re.finditer(r"^\| `(\w+)` \| ([\w_]+) \| (\w+) \| [^|]+ \| ([^|]+) \|", ledger.read_text(), re.MULTILINE):
        info[m.group(1)] = (m.group(2), m.group(3), m.group(4).strip())
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain-map")
    args = ap.parse_args()

    objs = load_objects()

    # ---------- link graph ----------
    lines = [
        "---",
        'type: "Ontology Link Graph"',
        'resource: "urn:ultracart:ontology:links"',
        "generated: true",
        "---",
        "",
        "# Link graph (generated — do not hand-edit; `python3 scripts/generate_indexes.py`)",
        "",
        "| From | Kind | To | On |",
        "|---|---|---|---|",
    ]
    for name, meta in sorted(objs.items()):
        for link in meta.get("links", []) or []:
            lines.append(f"| {name} | {link.get('kind','?')} | {link['to']} | `{link.get('on','')}` |")
    (ROOT / "links" / "link_graph.md").write_text("\n".join(lines) + "\n")

    # ---------- coverage ledger ----------
    table_info = parse_existing_ledger()
    table_info.update(parse_domain_map(args.domain_map))

    binding_to_obj = {}
    for name, meta in objs.items():
        binding_to_obj.setdefault(meta["source"]["binding"], []).append(name)

    catalog_tables = sorted({p.stem for p in CATALOG.glob("*.md")} - {"index"})
    rows = []
    counts = {"object source": 0, "streaming twin": 0, "peripheral": 0}
    for t in catalog_tables:
        domain, tier, meaning = table_info.get(t, ("?", "?", "?"))
        if t in binding_to_obj:
            role = "object source: " + ", ".join(f"`{o}`" for o in sorted(binding_to_obj[t]))
            counts["object source"] += 1
        elif t.endswith("_streaming") and t[: -len("_streaming")] in catalog_tables:
            role = f"streaming twin of `{t[:-10]}` (RecordTime/IsDelete change feed)"
            counts["streaming twin"] += 1
        else:
            role = "documented peripheral / property-link source"
            counts["peripheral"] += 1
        rows.append(f"| `{t}` | {domain} | {tier} | {role} | {meaning} |")

    header = [
        "---",
        'type: "Ontology Coverage Ledger"',
        'resource: "urn:ultracart:ontology:coverage"',
        "generated: true",
        "---",
        "",
        "# Coverage ledger — every canonical warehouse table, placed",
        "",
        f"Tables: {len(catalog_tables)} · object sources: {counts['object source']} · "
        f"streaming twins: {counts['streaming twin']} · peripheral/link sources: {counts['peripheral']}",
        "",
        "Totality is enforced by `validate_ontology.py --offline`. Regenerate with",
        "`python3 scripts/generate_indexes.py` after adding objects.",
        "",
        "| Table | Domain | Tier | Ontology role | Meaning |",
        "|---|---|---|---|---|",
    ]
    (ROOT / "links" / "coverage_ledger.md").write_text("\n".join(header + rows) + "\n")
    print(f"link_graph.md: {sum(len(m.get('links') or []) for m in objs.values())} links from {len(objs)} objects")
    print(f"coverage_ledger.md: {len(catalog_tables)} tables ({counts})")


if __name__ == "__main__":
    main()
