#!/usr/bin/env python3
"""Validate OKF v0.1 conformance plus project-specific quality gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RAW_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SECRET_RE = re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{20,}|xox[baprs]-[A-Za-z0-9-]+)\b")
RESERVED = {"index.md", "log.md"}
PRODUCER_REQUIRED = {"type", "title", "description", "resource", "timestamp"}


def parse_frontmatter(text: str) -> tuple[dict[str, object], str] | None:
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


def concept_paths(bundle: Path) -> list[Path]:
    return sorted(
        path
        for path in bundle.rglob("*.md")
        if path.name not in RESERVED
    )


def rel_id(bundle: Path, path: Path) -> str:
    return "/" + str(path.relative_to(bundle)).replace("\\", "/")


def check_frontmatter(bundle: Path, errors: list[str]) -> None:
    for path in concept_paths(bundle):
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if parsed is None:
            errors.append(f"{rel_id(bundle, path)}: missing parseable YAML frontmatter")
            continue
        fm, _ = parsed
        if not str(fm.get("type") or "").strip():
            errors.append(f"{rel_id(bundle, path)}: frontmatter.type is required")
        missing = sorted(key for key in PRODUCER_REQUIRED if not str(fm.get(key) or "").strip())
        if missing:
            errors.append(f"{rel_id(bundle, path)}: missing producer-required keys {missing}")


def check_reserved(bundle: Path, errors: list[str]) -> None:
    for path in sorted(bundle.rglob("index.md")):
        text = path.read_text(encoding="utf-8")
        if path == bundle / "index.md" and text.startswith("---\n"):
            parsed = parse_frontmatter(text)
            body = parsed[1] if parsed else ""
            fm = parsed[0] if parsed else {}
            if "okf_version" not in fm:
                errors.append("/index.md: root frontmatter is allowed only when declaring okf_version")
        elif text.startswith("---\n"):
            errors.append(f"{rel_id(bundle, path)}: non-root index.md must not contain frontmatter")
            body = text
        else:
            body = text
        if not re.search(r"^#\s+", body, re.M):
            errors.append(f"{rel_id(bundle, path)}: index.md should contain section headings")
    for path in sorted(bundle.rglob("log.md")):
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            errors.append(f"{rel_id(bundle, path)}: log.md must not contain frontmatter")
        if not re.search(r"^##\s+\d{4}-\d{2}-\d{2}\b", text, re.M):
            errors.append(f"{rel_id(bundle, path)}: log.md needs ISO date headings")


def resolve_link(bundle: Path, source: Path, target: str) -> Path | None:
    target = unquote(target.split("#", 1)[0])
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.endswith("/"):
        target = target + "index.md"
    if not target.endswith(".md"):
        return None
    if target.startswith("/"):
        return (bundle / target.lstrip("/")).resolve()
    return (source.parent / target).resolve()


def check_links(bundle: Path, errors: list[str]) -> None:
    root = bundle.resolve()
    for path in sorted(bundle.rglob("*.md")):
        body = path.read_text(encoding="utf-8")
        for _, target in LINK_RE.findall(body):
            resolved = resolve_link(bundle, path, target)
            if resolved is None:
                continue
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"{rel_id(bundle, path)}: link escapes bundle: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{rel_id(bundle, path)}: broken internal link: {target}")


def check_safety(bundle: Path, errors: list[str]) -> None:
    for path in sorted(bundle.rglob("*")):
        if path.is_dir() or path.name == "sanitized_bq_metadata.json":
            pass
        if path.suffix not in {".md", ".json", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        emails = [
            email
            for email in RAW_EMAIL_RE.findall(text)
            if not email.endswith("@example.com")
        ]
        if emails:
            errors.append(f"{rel_id(bundle, path)}: possible raw email value(s): {emails[:3]}")
        if SECRET_RE.search(text):
            errors.append(f"{rel_id(bundle, path)}: possible secret token")
        if "SELECT *" in text.upper():
            errors.append(f"{rel_id(bundle, path)}: unsafe SELECT * example")
    meta = bundle / "_source_metadata" / "sanitized_bq_metadata.json"
    if meta.exists() and '"query"' in meta.read_text(encoding="utf-8", errors="replace"):
        errors.append("/_source_metadata/sanitized_bq_metadata.json: view SQL query key should be omitted")


def check_coverage(bundle: Path, expected: int | None, errors: list[str]) -> None:
    summary_path = bundle / "_source_metadata" / "source_summary.json"
    if not summary_path.exists():
        errors.append("/_source_metadata/source_summary.json: missing source summary")
        return
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    object_count = int(summary.get("object_count", 0))
    concept_count = len(
        [
            path
            for path in (bundle / "tables").glob("*/*.md")
            if path.name != "index.md"
        ]
    )
    if concept_count != object_count:
        errors.append(f"table concept coverage mismatch: {concept_count} docs vs {object_count} metadata objects")
    if expected is not None and object_count != expected:
        errors.append(f"expected {expected} metadata objects, found {object_count}")
    dataset_docs = [
        path
        for path in (bundle / "datasets").glob("*.md")
        if path.name != "index.md"
    ]
    if int(summary.get("dataset_count", 0)) != len(dataset_docs):
        errors.append("dataset concept coverage mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an OKF bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--expect-table-count", type=int)
    args = parser.parse_args()
    bundle = args.bundle
    errors: list[str] = []

    if not bundle.exists():
        print(f"Bundle does not exist: {bundle}", file=sys.stderr)
        return 2

    check_frontmatter(bundle, errors)
    check_reserved(bundle, errors)
    check_links(bundle, errors)
    check_safety(bundle, errors)
    check_coverage(bundle, args.expect_table_count, errors)

    if errors:
        print("OKF validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    summary = json.loads((bundle / "_source_metadata" / "source_summary.json").read_text(encoding="utf-8"))
    print(
        "OKF validation passed: "
        f"{summary['dataset_count']} datasets, {summary['object_count']} table/view concepts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
