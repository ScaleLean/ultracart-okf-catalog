#!/usr/bin/env python3
"""Offline, idempotent migration of the tracked standard catalog and mirror."""
import json
from pathlib import Path
import re
import shutil
from okf_document import parse
from build_okf_viewer import load_bundle, build_html


def migrate(root):
    bundle = root / 'okf/ultracart_warehouse'
    changed = 0
    for path in sorted(bundle.rglob('*.md')):
        text = path.read_text()
        parsed = parse(text)
        if parsed and 'timestamp' in parsed[0]:
            stamp = parsed[0]['timestamp']
            text = re.sub(r'^timestamp:.*$', 'generated:\n  by: process:build_standard_okf_catalog\n  at: ' + json.dumps(stamp), text, flags=re.M)
        if path == bundle / 'index.md':
            text = text.replace('okf_version: "0.1"', 'okf_version: "0.2"')
        if text != path.read_text():
            path.write_text(text)
            changed += 1
    summary_path = bundle / '_source_metadata/source_summary.json'
    summary = json.loads(summary_path.read_text())
    summary['okf_version'] = '0.2'
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    (bundle / 'viz.html').write_text(build_html(bundle.name, load_bundle(bundle)))
    for name in ['concepts', 'datasets', 'references', 'tables', '_source_metadata']:
        shutil.copytree(bundle / name, root / name, dirs_exist_ok=True)
    for name in ['index.md', 'log.md', 'viz.html']:
        shutil.copyfile(bundle / name, root / name)
    print(f'Migrated {changed} Markdown files. Root mirror synchronized.')


if __name__ == '__main__':
    migrate(Path(__file__).resolve().parents[1])
