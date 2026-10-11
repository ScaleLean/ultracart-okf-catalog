#!/usr/bin/env python3
"""Build a merchant-neutral sidecar; separate from the conformant OKF 0.2 bundle."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'ontology/scripts'))
from compile_ontology import load_front_matter
from offline_contract import check_binding, DATASETS
from sql_syntax import ontology_dependencies
from audit_agent_usability import has_wildcard_projection

LIMITS = [
    'Historical dataset-specific metadata only; source capture time is unknown, legacy generation dates are retained as reported evidence.',
    'Direct property types and referenced field existence/types are checked; derived SQL output types are declared, not inferred or dry-run verified.',
    'No live freshness, permissions, tenant isolation, key uniqueness, join cardinality, identity coverage, PII safety or business-policy attestation.',
    'Definition dependencies, output declarations and wildcard projections are checked; full SQL column/type semantics are not validated.',
    'Ledger checks establish name coverage only, not exactly-once roles. Action guards are declarations, not runtime enforcement.',
    'Deployable compilation is refused; offline previews carry unresolved scope/grain and are for local review only.',
]


def dependencies(meta):
    return ontology_dependencies(meta['sql'])


def check_outputs(meta):
    """Check names in the final SELECT using a deliberately limited projection grammar.

    Types remain declarations; this does not establish SQL expression semantics.
    Unsupported projection syntax fails closed.
    """
    if has_wildcard_projection(meta['sql']):
        raise ValueError('wildcard projection forbidden, including nested SELECTs')
    sql = re.sub(r"--[^\n]*|/\*.*?\*/|'(?:[^']|'')*'|\"(?:[^\"\\]|\\.)*\"", ' ', meta['sql'], flags=re.DOTALL)
    if re.search(r'\bselect\s+(?:(?:distinct|all)\s+)?as\s+(?:struct|value)\b', sql, re.IGNORECASE):
        raise ValueError('unsupported SELECT AS STRUCT/VALUE modifier in definition outputs')
    tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|[^\s]', sql)
    depth, start, end = 0, None, None
    for i, token in enumerate(tokens):
        if token == '(':
            depth += 1
        elif token == ')':
            depth -= 1
        elif depth == 0 and token.lower() == 'select':
            start = i + 1
        elif depth == 0 and token.lower() == 'from' and start is not None:
            end = i
            break
    if start is None or end is None:
        raise ValueError('unsupported definition output projection')
    groups, current, depth = [], [], 0
    for token in tokens[start:end]:
        if token in ('(', '['):
            depth += 1
        elif token in (')', ']'):
            depth -= 1
        if token == ',' and depth == 0:
            groups.append(current)
            current = []
        else:
            current.append(token)
    groups.append(current)
    names = []
    for group in groups:
        if group and group[0].lower() in ('distinct', 'all'):
            group = group[1:]
        if len(group) >= 3 and group[-2].lower() == 'as':
            names.append(group[-1])
        elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', ''.join(group)):
            names.append(group[-1])
        else:
            raise ValueError('unsupported definition output syntax; use explicit aliases')
    if len(names) != len(set(names)) or set(names) != set(meta.get('outputs', {})):
        raise ValueError(f'definition output declaration mismatch: SQL {names}, declared {list(meta.get("outputs", {}))}')
    if any(t not in {'STRING', 'INTEGER', 'NUMERIC', 'BOOLEAN', 'DATE', 'DATETIME', 'TIMESTAMP', 'FLOAT'}
           for t in meta['outputs'].values()):
        raise ValueError('unsupported declared output type')


def check_definition_graph(objects, definitions):
    """Reject unresolved and cyclic dependencies before assigning structural trust."""
    names = set(objects) | set(definitions)
    for name, meta in definitions.items():
        if set(meta['dependencies']) - names:
            raise ValueError(f'{name}: unknown dependency')
    pending = {name: set(meta['dependencies']) & set(definitions)
               for name, meta in definitions.items()}
    while pending:
        ready = [name for name, deps in pending.items() if not deps.intersection(pending)]
        if not ready:
            raise ValueError(f'cyclic definition dependencies: {sorted(pending)}')
        for name in ready:
            del pending[name]


def validate_provenance(stored):
    """Validate recorded formats, without treating generation/base commit as freshness."""
    if not isinstance(stored, dict):
        raise ValueError('manifest must be a JSON object')
    stamp = stored.get('generated_at')
    if not isinstance(stamp, str) or not re.fullmatch(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', stamp):
        raise ValueError('malformed generated_at: timezone-aware ISO timestamp required')
    if not stamp.endswith('Z') and (int(stamp[-5:-3]) >= 24 or int(stamp[-2:]) >= 60):
        raise ValueError('malformed generated_at: invalid timezone offset')
    try:
        datetime.fromisoformat(stamp.replace('Z', '+00:00'))
    except ValueError as e:
        raise ValueError('malformed generated_at: invalid calendar timestamp') from e
    commit = stored.get('source_commit')
    if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-fA-F]{40}', commit):
        raise ValueError('malformed source_commit: 40 hexadecimal characters required')


def build_manifest(root=ROOT):
    root = Path(root)
    files = sorted((root / 'okf/ultracart_warehouse').rglob('*.md'))
    files += [root / 'okf/ultracart_warehouse/_source_metadata/source_summary.json']
    files += sorted((root / 'ontology').rglob('*.md'))
    files += sorted((root / 'ontology/scripts').glob('*.py'))
    files += [root / 'scripts/build_knowledge_manifest.py', root / 'scripts/build_standard_okf_catalog.py',
              root / 'scripts/audit_agent_usability.py']
    objects, definitions = {}, {}
    declared_names, urns = {}, {}
    def register(meta, kind, path):
        name, urn = meta[kind], meta['resource']
        if name in declared_names:
            raise ValueError(f'duplicate object/definition name {name}: {declared_names[name]} and {path}')
        if urn in urns:
            raise ValueError(f'duplicate object/definition URN {urn}: {urns[urn]} and {path}')
        declared_names[name], urns[urn] = path, path
    families = set(load_front_matter(root / 'ontology/identity/identity_spine.md').get('families', []))
    for path in sorted((root / 'ontology/objects').rglob('*.md')):
        meta = load_front_matter(path)
        register(meta, 'object', path)
        errors = check_binding(meta, {'dataset': DATASETS}, root)
        if meta['key'].get('identity_family') not in families:
            errors.append('unknown identity family')
        if errors:
            raise ValueError(f'{path.name}: ' + '; '.join(errors))
        objects[meta['object']] = {
            'resource': meta['resource'], 'version': meta['version'],
            'source': meta['source'], 'key': meta['key'], 'grain': meta['grain'],
            'pii': meta['pii'],
            'outputs': {p['name']: p['type'] for p in meta['properties']},
            'dependencies': [meta['source']['default_table']],
            'schema_evidence': 'tables/' + DATASETS[re.search(r'dataset\.(\w+)', meta['source']['default_table']).group(1)] + '/' + meta['source']['default_table'].split('.')[-1] + '.md',
            'source_path': str(path.relative_to(root)),
            'scope_state': 'filter_declared_unverified' if meta['source'].get('merchant_filter') else 'unresolved_no_merchant_filter',
            'grain_state': 'declared_uniqueness_unverified',
            'output_type_state': 'direct_checked_derived_declared',
        }
    for path in sorted((root / 'ontology/definitions').glob('*.md')):
        meta = load_front_matter(path)
        register(meta, 'definition', path)
        if not meta.get('outputs') or has_wildcard_projection(meta['sql']):
            raise ValueError(f'{path.name}: explicit outputs required; wildcard projection forbidden')
        check_outputs(meta)
        definitions[meta['definition']] = {
            'resource': meta['resource'], 'version': meta['version'],
            'dependencies': dependencies(meta), 'outputs': meta['outputs'],
            'output_type_state': 'declared_unverified',
            'source_path': str(path.relative_to(root)),
        }
    check_definition_graph(objects, definitions)
    hashes = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    # Include root schema evidence actually used by check_binding, so mirror changes
    # cannot masquerade as the hashed nested bundle.
    for meta in objects.values():
        path = root / meta['schema_evidence']
        hashes[meta['schema_evidence']] = hashlib.sha256(path.read_bytes()).hexdigest()
    summary = json.loads((root / 'okf/ultracart_warehouse/_source_metadata/source_summary.json').read_text())
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    return {
        'manifest_version': '1.0', 'okf_version': '0.2', 'ontology_version': '0.1',
        'generated_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'source_captured_at': None, 'verified_at': None,
        'historical_evidence': {'catalog_reported_generated_at': summary['generated_at'],
                                'ontology_reported_built_date': '2026-07-06',
                                'record': 'ontology/VALIDATION.md', 'state': 'historical_unverified'},
        'source_commit': commit, 'source_hashes': hashes,
        'trust': {'structural': 'offline_checks_passed', 'semantic': 'unverified', 'live': 'not_checked'},
        'validation_limits': LIMITS, 'objects': objects, 'definitions': definitions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--out', type=Path)
    mode.add_argument('--check', type=Path, help='Fail if stored inputs/contracts are stale; no regeneration.')
    args = parser.parse_args()
    manifest = build_manifest()
    if args.check:
        stored = json.loads(args.check.read_text())
        try:
            validate_provenance(stored)
        except ValueError as e:
            raise SystemExit(f'FAIL: {e}') from e
        # Generation and base commit are historical provenance, not a freshness gate.
        keys = ('manifest_version', 'okf_version', 'ontology_version', 'source_hashes',
                'objects', 'definitions', 'trust', 'validation_limits', 'historical_evidence',
                'source_captured_at', 'verified_at')
        if any(stored.get(key) != manifest[key] for key in keys):
            raise SystemExit('FAIL: stale source hashes or machine contracts; regenerate the sidecar after review.')
        print('PASS: stored source hashes/contracts match; semantic/live trust remains unverified.')
        return
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(f'Wrote {args.out}; structural checks passed, semantic/live trust unverified.')


if __name__ == '__main__':
    main()
