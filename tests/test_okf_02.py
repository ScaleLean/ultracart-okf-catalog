"""Offline conformance, producer, viewer, and catalog regression tests."""
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from okf_document import parse, serialize, upgrade, trust_tier, is_stale
from validate_okf_bundle import check_frontmatter, check_reserved
from build_okf_viewer import load_bundle, build_html

BUNDLE = ROOT / 'okf/ultracart_warehouse'


class FormatTests(unittest.TestCase):
    def test_nested_yaml_roundtrip(self):
        fm = {'type': 'Custom type', 'sources': [{'resource': '/other.md', 'usage_count': 4}],
              'generated': {'by': 'process:test', 'at': '2026-07-01T00:00:00Z'},
              'extension': {'nested': [True, 7]}}
        self.assertEqual(parse(serialize(fm, 'body'))[0], fm)

    def test_bad_yaml_rejected(self):
        for text in ['---\ntype: [\n---\n', '---\n- not-a-map\n---\n', '---\ntype: X']:
            self.assertIsNone(parse(text))

    def test_minimal_and_unknown_types_and_broken_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'a.md'
            p.write_text('---\ntype: Future Type\nunknown: 1\n---\n[future](/absent.md)\n')
            errors = []
            check_frontmatter(Path(tmp), errors, producer=False)
            check_reserved(Path(tmp), errors)
            self.assertEqual(errors, [])
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_okf_bundle.py'), tmp, '--conformance-only'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_type_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'a.md').write_text('---\ntitle: Missing type\n---\n')
            errors = []
            check_frontmatter(Path(tmp), errors, producer=False)
            self.assertTrue(errors)

    def test_reserved_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.md').write_text('---\nokf_version: "0.2"\n---\n# Index\n')
            (root / 'sub').mkdir()
            (root / 'sub/index.md').write_text('---\ntype: Wrong\n---\n# Index\n')
            errors = []
            check_reserved(root, errors)
            self.assertEqual(len(errors), 1)

    def test_migration_preserves_timestamp_and_sources(self):
        fm, body = upgrade({'type': 'Reference', 'timestamp': '2026-07-01T00:00:00Z'}, '# Body\n\n# Citations\n[1] [Docs](https://example.com/docs)\n', 'process:test')
        self.assertEqual(fm['generated']['at'], '2026-07-01T00:00:00Z')
        self.assertEqual(fm['sources'], [{'resource': 'https://example.com/docs', 'title': 'Docs'}])
        self.assertNotIn('Citations', body)
        self.assertNotIn('verified', fm)
        self.assertEqual(upgrade(fm, body, 'process:test'), (fm, body))

    def test_trust_and_staleness(self):
        self.assertEqual(trust_tier({}), 'unverified')
        self.assertEqual(trust_tier({'verified': {'by': 'process:test'}}), 'machine-confirmed')
        self.assertEqual(trust_tier({'verified': [{'by': 'human:reviewer'}]}), 'human-reviewed')
        self.assertFalse(is_stale({'stale_after': '2020-01-01'}))
        self.assertTrue(is_stale({'stale_after': '2020-01-01T00:00:00Z'}))

    def test_all_producer_writers(self):
        for name in ['build_ultracart_okf', 'augment_okf_scalelean_views']:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                module = importlib.import_module(name)
                path = Path(tmp) / 'concept.md'
                module.write_doc(path, {'type': 'Reference', 'timestamp': '2026-07-01T00:00:00Z'}, '# Citations\n[1] [Docs](https://example.com)\n')
                fm, body = parse(path.read_text())
                self.assertIsInstance(fm['generated'], dict)
                self.assertEqual(fm['sources'][0]['resource'], 'https://example.com')
                self.assertNotIn('timestamp', fm)
        from build_standard_okf_catalog import yaml_frontmatter, OKF_VERSION
        self.assertEqual(OKF_VERSION, '0.2')
        self.assertIsInstance(parse(yaml_frontmatter({'type': 'Reference', 'timestamp': '2026-07-01T00:00:00Z'}))[0]['generated'], dict)

    def test_viewer_safe_nested_payload(self):
        html = build_html('test', {'docs': [{'body': '</script><script>alert(1)</script>'}], 'edges': []})
        self.assertNotIn('</script><script>alert', html)
        self.assertIn('\\u003c', html)


class CatalogTests(unittest.TestCase):
    def test_counts_and_mirror(self):
        summary = json.loads((BUNDLE / '_source_metadata/source_summary.json').read_text())
        self.assertEqual((summary['dataset_count'], summary['object_count'], summary['canonical_table_count']), (8, 244, 112))
        self.assertEqual(summary['okf_version'], '0.2')
        paths = [p for p in BUNDLE.rglob('*') if p.is_file()]
        for path in paths:
            self.assertEqual(path.read_bytes(), (ROOT / path.relative_to(BUNDLE)).read_bytes(), str(path))
        docs = load_bundle(BUNDLE)['docs']
        self.assertEqual(len(docs), 370)
        for doc in docs:
            self.assertNotIn('timestamp', doc['frontmatter'])
            self.assertEqual(doc['trust'], 'unverified')
            self.assertEqual(doc['frontmatter']['generated']['at'], '2026-07-01T00:00:00Z')

    def test_preserved_metadata_and_bodies(self):
        manifest = json.loads((ROOT / 'tests/catalog_baseline.json').read_text())
        actual = {}
        for path in BUNDLE.rglob('*.md'):
            if path.name in {'index.md', 'log.md'}:
                continue
            fm, body = parse(path.read_text())
            fm['timestamp'] = fm.pop('generated')['at']
            content = json.dumps([fm, body], sort_keys=True, ensure_ascii=False)
            actual[str(path.relative_to(BUNDLE))] = str(int.from_bytes(hashlib.sha256(content.encode()).digest(), 'big'))
        self.assertEqual(actual, manifest['concept_hashes'])
        summary = json.loads((BUNDLE / '_source_metadata/source_summary.json').read_text())
        summary['okf_version'] = '0.1'
        self.assertEqual(summary, manifest['summary'])


if __name__ == '__main__':
    unittest.main()
