#!/usr/bin/env python3
"""Validate with the pinned Google reference document implementation, offline."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys

UPSTREAM_SHA = 'ad30107c31c06aec8a7d5636e0d1058118604e6f'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('upstream', type=Path)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    sha = subprocess.check_output(['git', '-C', str(args.upstream), 'rev-parse', 'HEAD'], text=True).strip()
    if sha != UPSTREAM_SHA:
        parser.error(f'Expected upstream {UPSTREAM_SHA}, found {sha}')
    source = args.upstream / 'src/reference_agent/bundle/document.py'
    spec = importlib.util.spec_from_file_location('google_okf_document', source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    count = 0
    for path in sorted(args.bundle.rglob('*.md')):
        if path.name in {'index.md', 'log.md'}:
            continue
        doc = module.OKFDocument.parse(path.read_text())
        doc.validate()
        count += 1
    print(f'Google reference validation passed: {count} concepts, upstream {sha}.')


if __name__ == '__main__':
    main()
