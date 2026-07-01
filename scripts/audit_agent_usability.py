#!/usr/bin/env python3
"""Audit the UltraCart OKF repository for AI-agent usability."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CATALOG_DIRS = ["_source_metadata", "concepts", "datasets", "references", "tables"]
CATALOG_FILES = ["index.md", "log.md", "viz.html"]
CATALOG_MARKDOWN_DIRS = ["concepts", "datasets", "references", "tables"]
REQUIRED_FRONTMATTER = {"type", "title", "description", "resource", "timestamp"}
FORBIDDEN_TERMS = [
    "".join(chr(code) for code in [99, 101, 102]),
    "".join(chr(code) for code in [99, 108, 105, 110, 105, 99, 97, 108]),
]
CUSTOM_WORK_DATASET = "_".join(["ultracart", "dw", "work"])


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str] | None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    raw, body = match.groups()
    data: dict[str, object] = {}
    current: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current:
            data.setdefault(current, [])
            if isinstance(data[current], list):
                data[current].append(line[4:].strip().strip('"'))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = value.strip('"')
            current = None
        else:
            data[key] = []
            current = key
    return data, body


def rel(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def root_catalog_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for name in CATALOG_FILES:
        files.append(root / name)
    for dirname in CATALOG_DIRS:
        files.extend(sorted((root / dirname).rglob("*")))
    return [path for path in files if path.is_file()]


def resolve_link(root: Path, source: Path, target: str) -> Path | None:
    target = unquote(target.split("#", 1)[0])
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if target.endswith("/"):
        target += "index.md"
    if not target.endswith((".md", ".html", ".json")):
        return None
    if target.startswith("/"):
        return root / target.lstrip("/")
    return (source.parent / target).resolve()


def check_mirror(root: Path, bundle: Path, errors: list[str]) -> tuple[int, int]:
    checked = 0
    mismatched = 0
    for dirname in CATALOG_DIRS:
        for source in sorted((bundle / dirname).rglob("*")):
            if not source.is_file():
                continue
            checked += 1
            target = root / dirname / source.relative_to(bundle / dirname)
            if not target.exists():
                errors.append(f"missing root mirror: {rel(bundle, source)}")
                mismatched += 1
            elif source.read_bytes() != target.read_bytes():
                errors.append(f"root mirror differs: {rel(bundle, source)}")
                mismatched += 1
    for name in CATALOG_FILES:
        checked += 1
        source = bundle / name
        target = root / name
        if not source.exists() or not target.exists():
            errors.append(f"missing mirrored catalog file: {name}")
            mismatched += 1
        elif source.read_bytes() != target.read_bytes():
            errors.append(f"root mirror differs: {name}")
            mismatched += 1
    return checked, mismatched


def check_frontmatter(root: Path, errors: list[str]) -> int:
    concept_count = 0
    for dirname in CATALOG_MARKDOWN_DIRS:
        for path in sorted((root / dirname).rglob("*.md")):
            if path.name in {"index.md", "log.md"}:
                continue
            concept_count += 1
            parsed = parse_frontmatter(path)
            if parsed is None:
                errors.append(f"{rel(root, path)}: missing parseable frontmatter")
                continue
            frontmatter, _ = parsed
            missing = sorted(key for key in REQUIRED_FRONTMATTER if not str(frontmatter.get(key) or "").strip())
            if missing:
                errors.append(f"{rel(root, path)}: missing frontmatter keys {missing}")
    return concept_count


def check_links(root: Path, errors: list[str]) -> int:
    checked = 0
    markdown_files = [
        root / "README.md",
        root / "index.md",
        *sorted((root / "concepts").rglob("*.md")),
        *sorted((root / "datasets").rglob("*.md")),
        *sorted((root / "references").rglob("*.md")),
        *sorted((root / "tables").rglob("*.md")),
    ]
    for path in markdown_files:
        if not path.exists():
            continue
        for _, target in LINK_RE.findall(path.read_text(encoding="utf-8")):
            resolved = resolve_link(root, path, target)
            if resolved is None:
                continue
            checked += 1
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{rel(root, path)}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{rel(root, path)}: broken internal link: {target}")
    return checked


def check_table_docs(root: Path, summary: dict[str, object], errors: list[str]) -> int:
    table_docs = sorted(path for path in (root / "tables").glob("*/*.md") if path.name != "index.md")
    expected = int(summary["object_count"])
    if len(table_docs) != expected:
        errors.append(f"expected {expected} root table docs, found {len(table_docs)}")
    for path in table_docs:
        text = path.read_text(encoding="utf-8")
        for section in ["## Definition", "## Schema Coverage", "## Field Paths", "## Query Pattern", "## References"]:
            if section not in text:
                errors.append(f"{rel(root, path)}: missing {section}")
        if "{{ source_project }}" not in text:
            errors.append(f"{rel(root, path)}: missing source_project query placeholder")
    return len(table_docs)


def check_safety(root: Path, errors: list[str]) -> int:
    scanned = 0
    for path in sorted(root.rglob("*")):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json", ".html", ".py", ".sql", ".yml", ".yaml", ".gitignore"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for term in FORBIDDEN_TERMS:
            if term in text:
                errors.append(f"{rel(root, path)}: forbidden merchant-specific term found")
                break
        if path.suffix.lower() != ".py" and "select *" in text:
            errors.append(f"{rel(root, path)}: unsafe SELECT star pattern")
    return scanned


def check_required_paths(root: Path, errors: list[str]) -> None:
    required = [
        root / "tables" / "ultracart_dw_medium" / "uc_affiliate_clicks.md",
        root / "tables" / "ultracart_dw_medium" / "uc_orders.md",
        root / "concepts" / "tables_by_name" / "uc_orders.md",
        root / "datasets" / "ultracart_dw_medium.md",
        root / "references" / "bigquery_usage.md",
        root / "viz.html",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"required agent entrypoint missing: {rel(root, path)}")
    if (root / "tables" / CUSTOM_WORK_DATASET).exists():
        errors.append("custom work dataset must not be published as standard catalog")
    if (root / "okf" / "ultracart_warehouse" / "tables" / CUSTOM_WORK_DATASET).exists():
        errors.append("custom work dataset must not be published in nested standard bundle")


def write_report(path: Path, stats: dict[str, object], errors: list[str]) -> None:
    lines = [
        "# Agent Usability Audit",
        "",
        "This report checks whether the repository is directly usable by AI agents reading GitHub paths and OKF Markdown concepts.",
        "",
        "## Result",
        "",
        "PASS" if not errors else "FAIL",
        "",
        "## Coverage",
        "",
    ]
    for key, value in stats.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Gates", ""])
    gates = [
        "Root catalog mirror matches the validated nested OKF bundle.",
        "All root catalog concept pages have parseable OKF frontmatter.",
        "All internal Markdown links resolve against repository-root GitHub paths.",
        "Every dataset-specific table page has definition, schema coverage, field paths, query pattern, and references.",
        "Expected agent entrypoints exist at root-level GitHub paths.",
        "Safety scan found no merchant-specific forbidden terms or unsafe SELECT star examples.",
    ]
    for gate in gates:
        lines.append(f"- {gate}")
    lines.extend(["", "## Errors", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- None.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repo-wide AI-agent usability for the UltraCart OKF catalog.")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--bundle", type=Path, default=Path("okf/ultracart_warehouse"))
    parser.add_argument("--report", type=Path, default=Path("reports/agent_usability_audit.md"))
    args = parser.parse_args()
    root = args.root.resolve()
    bundle = (root / args.bundle).resolve()
    report = root / args.report
    errors: list[str] = []

    summary_path = root / "_source_metadata" / "source_summary.json"
    if not summary_path.exists():
        errors.append("missing root source summary")
        summary: dict[str, object] = {"object_count": 0}
    else:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))

    mirrored_count, mirror_mismatches = check_mirror(root, bundle, errors)
    concept_count = check_frontmatter(root, errors)
    link_count = check_links(root, errors)
    table_doc_count = check_table_docs(root, summary, errors)
    safety_file_count = check_safety(root, errors)
    check_required_paths(root, errors)

    stats = {
        "datasets": summary.get("dataset_count", 0),
        "dataset_specific_objects": summary.get("object_count", 0),
        "canonical_table_definitions": summary.get("canonical_table_count", 0),
        "root_table_docs": table_doc_count,
        "root_concept_docs": concept_count,
        "internal_links_checked": link_count,
        "mirrored_files_checked": mirrored_count,
        "mirror_mismatches": mirror_mismatches,
        "safety_files_scanned": safety_file_count,
    }
    write_report(report, stats, errors)
    if errors:
        print(f"Agent usability audit failed. Wrote {report}")
        for error in errors[:50]:
            print(f"- {error}")
        if len(errors) > 50:
            print(f"- ... {len(errors) - 50} more")
        return 1
    print(f"Agent usability audit passed. Wrote {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
