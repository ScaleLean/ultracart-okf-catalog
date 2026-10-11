"""Merchant-neutral offline behavioral regressions; fixtures are not live evidence."""
import json
import re
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'ontology/scripts'))
import audit_agent_usability as audit
import compile_ontology as compiler


class WildcardTests(unittest.TestCase):
    def test_projection_wildcards(self):
        for sql in ('SELECT * FROM t', 'SELECT mc.* FROM t mc',
                    'SELECT x, t.* EXCEPT(secret) FROM t',
                    'WITH q AS (SELECT /* gap */ DISTINCT * FROM t) SELECT x FROM q'):
            with self.subTest(sql=sql):
                self.assertTrue(audit.has_wildcard_projection(sql))
        for sql in ('SELECT COUNT(*) AS n FROM t', 'SELECT x * y AS total FROM t',
                    "SELECT 'SELECT * FROM t' AS text FROM t", '-- SELECT * FROM t\nSELECT x FROM t'):
            with self.subTest(sql=sql):
                self.assertFalse(audit.has_wildcard_projection(sql))

    def test_failed_report_does_not_claim_safety_pass(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'report.md'
            audit.write_report(path, {}, ['unsafe projection'])
            self.assertNotIn('Safety scan found no', path.read_text())
            self.assertIn('FAIL', path.read_text())


class ProvenanceTests(unittest.TestCase):
    def test_standard_build_separates_unknown_capture_from_generation(self):
        import subprocess
        from datetime import datetime, timezone
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            inventory = d / 'inventory.csv'
            inventory.write_text('table_schema,table_name,table_type\nultracart_dw_medium,uc_orders,VIEW\n')
            start = datetime.now(timezone.utc)
            subprocess.run([sys.executable, str(ROOT / 'scripts/build_standard_okf_catalog.py'),
                            '--table-inventory', str(inventory), '--out', str(d / 'bundle')], check=True,
                           capture_output=True, text=True)
            summary = json.loads((d / 'bundle/_source_metadata/source_summary.json').read_text())
            self.assertGreaterEqual(datetime.fromisoformat(summary['generated_at'].replace('Z', '+00:00')), start)
            self.assertIsNone(summary['source_captured_at'])
            self.assertIsNone(summary['verified_at'])
            self.assertEqual(summary['verification_state'], 'unverified')
            import hashlib
            self.assertEqual(summary['source_hashes']['table_inventory'], hashlib.sha256(inventory.read_bytes()).hexdigest())


CFG = {'source_project': 'offline-source', 'merchant_id': 'DEMO',
       'ontology_project': 'offline-output', 'ontology_dataset': 'ontology',
       'dataset': {'medium': 'ultracart_dw_medium'}}


def fixture_object():
    return {'object': 'sample', 'resource': 'urn:test:sample', 'version': 1,
            'grain': 'one row per id', 'key': {'fields': ['id']},
            'source': {'default_table': '{{source_project}}.{{dataset.medium}}.sample',
                       'merchant_filter': "merchant_id = '{{merchant_id}}'"},
            'properties': [{'name': 'id', 'type': 'STRING', 'source': 'id'}]}


class BindingTests(unittest.TestCase):
    def test_override_never_removes_filter(self):
        cfg = dict(CFG, bindings={'sample': 'offline-source.other.sample'})
        with self.assertRaisesRegex(ValueError, 'override'):
            compiler.compile_object(fixture_object(), cfg)

    def test_selected_dataset_missing_fields_and_types(self):
        import offline_contract as contract
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            doc = root / 'tables/ultracart_dw_medium/sample.md'
            doc.parent.mkdir(parents=True)
            doc.write_text('| `id` | `STRING` |\n| `merchant_id` | `STRING` |\n')
            meta = fixture_object()
            self.assertEqual(contract.check_binding(meta, CFG, root), [])
            # A cross-tier union exists but cannot rescue the selected tier.
            union = root / 'concepts/tables_by_name/sample.md'
            union.parent.mkdir(parents=True)
            union.write_text(doc.read_text())
            doc.write_text('| `merchant_id` | `STRING` |\n')
            self.assertTrue(any('id' in e for e in contract.check_binding(meta, CFG, root)))
            doc.write_text('| `id` | `INTEGER` |\n| `merchant_id` | `STRING` |\n')
            self.assertTrue(any('type' in e for e in contract.check_binding(meta, CFG, root)))

    def test_unknown_streaming_scope_and_grain_rejected(self):
        import offline_contract as contract
        for dataset in ('ultracart_dw_streaming', 'unknown', 'ultracart_dw_linked'):
            with self.subTest(dataset=dataset):
                cfg = dict(CFG, dataset={'medium': dataset})
                self.assertTrue(contract.check_binding(fixture_object(), cfg, ROOT))
        meta = fixture_object()
        meta.pop('grain')
        self.assertTrue(any('grain' in e for e in contract.check_binding(meta, CFG, ROOT)))

    def test_default_compiler_refuses_unestablished_grain(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'config.yml'
            import yaml
            path.write_text(yaml.safe_dump(CFG))
            res = subprocess.run([sys.executable, str(ROOT / 'ontology/scripts/compile_ontology.py'),
                                  '--config', str(path), '--stdout'], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn('grain', res.stderr.lower())
            self.assertNotIn('CREATE', res.stdout)


class ManifestTests(unittest.TestCase):
    def test_machine_manifest_hashes_dependencies_and_trust(self):
        import hashlib
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'manifest.json'
            res = subprocess.run([sys.executable, str(ROOT / 'scripts/build_knowledge_manifest.py'),
                                  '--out', str(path)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            data = json.loads(path.read_text())
            self.assertEqual(data['manifest_version'], '1.0')
            self.assertEqual(data['okf_version'], '0.2')
            self.assertEqual(data['trust']['semantic'], 'unverified')
            self.assertIsNone(data['verified_at'])
            self.assertIsNone(data['source_captured_at'])
            self.assertTrue(data['validation_limits'])
            self.assertEqual(data['definitions']['customer']['dependencies'], ['revenue_order'])
            self.assertEqual(data['definitions']['customer']['outputs']['lifetime_total'], 'NUMERIC')
            for key, digest in data['source_hashes'].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / key).read_bytes()).hexdigest())

    def test_preview_outputs_and_excluded_dependency_failure(self):
        import subprocess
        import yaml
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            config = d / 'config.yml'
            config.write_text(yaml.safe_dump(CFG))
            cmd = [sys.executable, str(ROOT / 'ontology/scripts/compile_ontology.py'),
                   '--config', str(config), '--offline-preview', '--out', str(d / 'out')]
            res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            data = json.loads((d / 'out/manifest.json').read_text())
            self.assertEqual(data['manifest_version'], '1.0')
            self.assertFalse(data['deployable'])
            self.assertEqual(data['definitions']['repeat_customer']['dependencies'], ['customer'])
            self.assertEqual(data['objects']['order']['output_types']['total'], 'NUMERIC')
            sql = (d / 'out/ontology_views.sql').read_text()
            self.assertIn("WHERE merchant_id = 'DEMO'", sql)
            self.assertIn('UNVERIFIED OFFLINE REVIEW', sql)
            self.assertNotIn('{{', sql)
            self.assertLess(sql.index('.revenue_order`\nOPTIONS'), sql.index('.customer`\nOPTIONS'))
            config.write_text(yaml.safe_dump(dict(CFG, exclude_objects=['order'])))
            res = subprocess.run(cmd[:-1] + [str(d / 'failed')], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn('dependency', res.stderr)
            self.assertFalse((d / 'failed').exists())


class OutputContractTests(unittest.TestCase):
    def test_definition_output_drift_is_rejected(self):
        import build_knowledge_manifest as knowledge
        meta = {'sql': 'SELECT id, COUNT(*) AS n FROM {{ontology}}.sample GROUP BY id',
                'outputs': {'id': 'STRING', 'count': 'INTEGER'}}
        with self.assertRaisesRegex(ValueError, 'output'):
            knowledge.check_outputs(meta)
        meta['outputs'] = {'id': 'STRING', 'n': 'INTEGER'}
        knowledge.check_outputs(meta)


class IdentityTests(unittest.TestCase):
    def test_all_declared_identity_families_are_documented(self):
        families = compiler.load_front_matter(ROOT / 'ontology/identity/identity_spine.md').get('families', [])
        for path in (ROOT / 'ontology/objects').rglob('*.md'):
            meta = compiler.load_front_matter(path)
            self.assertIn(meta['key']['identity_family'], families)


class StoredManifestTests(unittest.TestCase):
    def test_manifest_check_rejects_stale_hashes(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'manifest.json'
            script = str(ROOT / 'scripts/build_knowledge_manifest.py')
            subprocess.run([sys.executable, script, '--out', str(path)], check=True, capture_output=True)
            res = subprocess.run([sys.executable, script, '--check', str(path)], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, res.stderr)
            data = json.loads(path.read_text())
            data['source_hashes']['ontology/definitions/customer.md'] = 'stale'
            path.write_text(json.dumps(data))
            res = subprocess.run([sys.executable, script, '--check', str(path)], capture_output=True, text=True)
            self.assertNotEqual(res.returncode, 0)
            self.assertIn('stale', res.stderr.lower())

    def test_quoted_yaml_sql_is_audited(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'definition.md').write_text('---\ntype: Ontology Definition\nsql: "SELECT t.* FROM t"\n---\n')
            errors = []
            audit.check_safety(root, errors)
            self.assertTrue(any('star' in error for error in errors))


class DigestAuditTests(unittest.TestCase):
    def test_hex_source_hashes_do_not_trigger_merchant_substrings(self):
        import hashlib
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            # Synthetic digest chosen to exercise the substring collision.
            digest = next(hashlib.sha256(str(i).encode()).hexdigest() for i in range(10000)
                          if audit.FORBIDDEN_TERMS[0] in hashlib.sha256(str(i).encode()).hexdigest())
            path = root / 'manifest.json'
            path.write_text(json.dumps({'source_hashes': {'source.md': digest}}))
            errors = []
            audit.check_safety(root, errors)
            self.assertEqual(errors, [])
            path.write_text(json.dumps({'source_hashes': {'source.md': audit.FORBIDDEN_TERMS[0]}}))
            audit.check_safety(root, errors)
            self.assertTrue(errors)


class GeneratedCatalogTests(unittest.TestCase):
    def test_new_build_is_okf_conformant(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            inventory = root / 'inventory.csv'
            inventory.write_text('table_schema,table_name,table_type\nultracart_dw_medium,uc_orders,VIEW\n')
            subprocess.run([sys.executable, str(ROOT / 'scripts/build_standard_okf_catalog.py'),
                            '--table-inventory', str(inventory), '--out', str(root / 'catalog')],
                           check=True, capture_output=True)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_okf_bundle.py'),
                                     str(root / 'catalog'), '--conformance-only'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class ReviewWildcardTests(unittest.TestCase):
    def test_nested_modifier_wildcards_are_detected_and_rejected(self):
        import build_knowledge_manifest as knowledge
        for projection in ('AS STRUCT *', 'AS VALUE *', 'DISTINCT AS STRUCT *',
                           'AS STRUCT o.*', 'AS VALUE /* gap */ o.*'):
            sql = ('SELECT (SELECT ' + projection + ' FROM {{ontology}}.order o LIMIT 1) '
                   'AS payload FROM {{ontology}}.order')
            with self.subTest(projection=projection):
                self.assertTrue(audit.has_wildcard_projection(sql))
                with self.assertRaisesRegex(ValueError, 'wildcard|modifier'):
                    knowledge.check_outputs({'sql': sql, 'outputs': {'payload': 'STRING'}})

    def test_unsupported_modifier_even_without_star_fails_closed(self):
        import build_knowledge_manifest as knowledge
        sql = 'SELECT (SELECT AS STRUCT order_id FROM {{ontology}}.order LIMIT 1) AS payload FROM {{ontology}}.order'
        with self.assertRaisesRegex(ValueError, 'modifier'):
            knowledge.check_outputs({'sql': sql, 'outputs': {'payload': 'STRING'}})


class ReviewDirectSourceTests(unittest.TestCase):
    def test_explicit_refs_cannot_hide_missing_direct_source(self):
        import copy
        import offline_contract as contract
        from unittest.mock import patch
        original = compiler.load_front_matter(ROOT / 'ontology/objects/commerce_core/order.md')
        for source in ('missing_column_not_in_schema', '`missing_column_not_in_schema`',
                       '  missing_column_not_in_schema  ',
                       '`missing_column_not_in_schema`.`leaf`', '`true`'):
            with self.subTest(source=source):
                meta = copy.deepcopy(original)
                meta['properties'][0].update(source=source, refs=['order_id'])
                errors = contract.check_binding(meta, CFG, ROOT)
                expected = source.replace('`', '').strip()
                self.assertTrue(any(expected in e for e in errors), errors)
                with self.assertRaisesRegex(ValueError, re.escape(expected)):
                    compiler.compile_object(meta, CFG, offline_preview=True)
                # The CLI must refuse before it writes any preview output too.
                import build_knowledge_manifest as knowledge
                with patch.object(knowledge, 'load_front_matter', side_effect=lambda p:
                                  meta if p.name == 'order.md' else compiler.load_front_matter(p)):
                    with self.assertRaisesRegex(ValueError, re.escape(expected)):
                        knowledge.build_manifest()

    def test_direct_type_checked_even_with_different_explicit_refs(self):
        import offline_contract as contract
        for source in ('customer_profile.customer_profile_oid',
                       '`customer_profile.customer_profile_oid`',
                       '`customer_profile`.`customer_profile_oid`'):
            with self.subTest(source=source):
                meta = compiler.load_front_matter(ROOT / 'ontology/objects/commerce_core/order.md')
                meta['properties'][0].update(source=source, refs=['order_id'])
                errors = contract.check_binding(meta, CFG, ROOT)
                self.assertTrue(any('type mismatch' in e for e in errors), errors)
                with self.assertRaisesRegex(ValueError, 'type mismatch'):
                    compiler.compile_object(meta, CFG, offline_preview=True)


class ReviewManifestGraphTests(unittest.TestCase):
    def test_duplicate_object_definition_names_and_urns_rejected(self):
        import copy
        import build_knowledge_manifest as knowledge
        from unittest.mock import patch
        cases = [
            ('objects/affiliates/affiliate_click.md', 'object', 'affiliate_ledger'),
            ('objects/affiliates/affiliate_click.md', 'object', 'active_subscriber'),
            ('definitions/active_subscriber.md', 'definition', 'paused_subscriber'),
            ('definitions/active_subscriber.md', 'resource', 'urn:ultracart:ontology:definition:paused_subscriber'),
            ('definitions/active_subscriber.md', 'resource', 'urn:ultracart:ontology:object:order'),
            ('objects/affiliates/affiliate_click.md', 'resource', 'urn:ultracart:ontology:object:affiliate_ledger'),
        ]
        for suffix, key, value in cases:
            with self.subTest(suffix=suffix, key=key, value=value):
                def altered(path):
                    meta = copy.deepcopy(compiler.load_front_matter(path))
                    if str(path).endswith(suffix):
                        meta[key] = value
                    return meta
                with patch.object(knowledge, 'load_front_matter', side_effect=altered):
                    with self.assertRaisesRegex(ValueError, 'duplicate'):
                        knowledge.build_manifest()

    def test_self_and_mutual_definition_cycles_rejected(self):
        import build_knowledge_manifest as knowledge
        from unittest.mock import patch
        for mutual in (False, True):
            with self.subTest(mutual=mutual):
                def altered(path):
                    meta = compiler.load_front_matter(path)
                    if path.name == 'customer.md':
                        meta['sql'] = meta['sql'].replace('.revenue_order', '.repeat_customer' if mutual else '.customer')
                    return meta
                with patch.object(knowledge, 'load_front_matter', side_effect=altered):
                    with self.assertRaisesRegex(ValueError, 'cyclic|circular'):
                        knowledge.build_manifest()


class ReviewManifestProvenanceTests(unittest.TestCase):
    def test_check_rejects_malformed_provenance_but_accepts_historical_values(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'manifest.json'
            script = str(ROOT / 'scripts/build_knowledge_manifest.py')
            subprocess.run([sys.executable, script, '--out', str(path)], check=True, capture_output=True)
            original = json.loads(path.read_text())
            for key, value in [('generated_at', None), ('generated_at', 'not-a-date'),
                               ('generated_at', '2001-02-30T00:00:00Z'),
                               ('generated_at', '2001-01-01T00:00:00'),
                               ('source_commit', None), ('source_commit', 'not-a-commit'),
                               ('source_commit', 'g' * 40)]:
                with self.subTest(key=key, value=value):
                    path.write_text(json.dumps(dict(original, **{key: value})))
                    result = subprocess.run([sys.executable, script, '--check', str(path)], capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(key, result.stderr)
            path.write_text(json.dumps(dict(original, generated_at='2001-01-01T00:00:00Z', source_commit='0' * 40)))
            result = subprocess.run([sys.executable, script, '--check', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)


class SecondReviewDirectTests(unittest.TestCase):
    def test_formatting_cannot_hide_direct_missing_fields_or_types(self):
        import offline_contract as contract
        import build_knowledge_manifest as knowledge
        from unittest.mock import patch
        cases = [
            ('customer_profile . customer_profile_oid', 'type mismatch'),
            ('`customer_profile` . `customer_profile_oid`', 'type mismatch'),
            ('(customer_profile.customer_profile_oid)', 'type mismatch'),
            ('(`customer_profile.customer_profile_oid`)', 'type mismatch'),
            ('((`missing_column_not_in_schema`))', 'missing_column_not_in_schema'),
            ('(( `customer_profile` /* gap */ . `customer_profile_oid` ))', 'type mismatch'),
            ('(missing_column_not_in_schema)', 'missing_column_not_in_schema'),
        ]
        for source, diagnostic in cases:
            with self.subTest(source=source):
                meta = compiler.load_front_matter(ROOT / 'ontology/objects/commerce_core/order.md')
                meta['properties'][0].update(source=source, refs=['order_id'])
                errors = contract.check_binding(meta, CFG, ROOT)
                self.assertTrue(any(diagnostic in e for e in errors), errors)
                with self.assertRaisesRegex(ValueError, diagnostic):
                    compiler.compile_object(meta, CFG, offline_preview=True)
                with patch.object(knowledge, 'load_front_matter', side_effect=lambda p:
                                  meta if p.name == 'order.md' else compiler.load_front_matter(p)):
                    with self.assertRaisesRegex(ValueError, diagnostic):
                        knowledge.build_manifest()

    def test_valid_formatted_fields_and_unclassifiable_sources(self):
        import offline_contract as contract
        for source in ('(( order_id ))', '(`order_id`)', 'order_id /* trailing */'):
            with self.subTest(source=source):
                meta = compiler.load_front_matter(ROOT / 'ontology/objects/commerce_core/order.md')
                meta['properties'][0].update(source=source, refs=['order_id'])
                self.assertEqual(contract.check_binding(meta, CFG, ROOT), [])
        for source in ('order_id other_name', '(order_id', 'order_id .', 'order_id[0]',
                       'unreviewed_function(order_id)', '`order_id'):
            with self.subTest(source=source):
                meta = compiler.load_front_matter(ROOT / 'ontology/objects/commerce_core/order.md')
                meta['properties'][0].update(source=source, refs=['order_id'])
                self.assertTrue(contract.check_binding(meta, CFG, ROOT))


class SecondReviewReferenceTests(unittest.TestCase):
    variants = ('{{ontology}}.order', '`{{ontology}}.order`', '`{{ontology}}`.order',
                '{{ontology}}.`order`', '`{{ontology}}`.`order`',
                '`{{ontology}}` . `order`', '{{ontology}} /* left */ . -- right\n `order`')

    def test_extraction_and_rewriting_share_all_supported_variants(self):
        import build_knowledge_manifest as knowledge
        for ref in self.variants:
            with self.subTest(ref=ref):
                meta = {'definition': 'probe', 'version': 1, 'resource': 'urn:test:probe',
                        'sql': f'SELECT order_id FROM {ref}', 'outputs': {'order_id': 'STRING'}}
                self.assertEqual(knowledge.dependencies(meta), ['order'])
                sql = compiler.compile_definition(meta, CFG)
                self.assertIn('FROM `offline-output.ontology.order`', sql)
                self.assertNotIn('{{ontology}}', sql)

    def test_literals_and_comments_are_not_dependencies_or_rewritten(self):
        import build_knowledge_manifest as knowledge
        sql = "SELECT '{{ontology}}.unknown' AS label FROM `{{ontology}}`.`order` -- {{ontology}}.ignored\n"
        meta = {'definition': 'probe', 'version': 1, 'resource': 'urn:test:probe', 'sql': sql}
        self.assertEqual(knowledge.dependencies(meta), ['order'])
        compiled = compiler.compile_definition(meta, CFG)
        self.assertIn("'{{ontology}}.unknown'", compiled)
        self.assertIn('-- {{ontology}}.ignored', compiled)

    def test_unsupported_ontology_reference_shapes_rejected_consistently(self):
        import build_knowledge_manifest as knowledge
        for ref in ('{{ontology}}', '{{ontology}}[order]', '{{ontology}}.order.extra',
                    '`{{ontology}}.order$decorator`', '{{ontology}} .',
                    'prefix{{ontology}}.order', '{{ontology}}..order',
                    'other . {{ontology}}.order', '"{{ontology}}"."order"',
                    '"{{ontology}}.order"', "'{{ontology}}.order'"):
            with self.subTest(ref=ref):
                meta = {'definition': 'probe', 'version': 1, 'resource': 'urn:test:probe',
                        'sql': f'SELECT order_id FROM {ref}', 'outputs': {'order_id': 'STRING'}}
                with self.assertRaisesRegex(ValueError, 'ontology reference'):
                    knowledge.dependencies(meta)
                with self.assertRaisesRegex(ValueError, 'ontology reference'):
                    compiler.compile_definition(meta, CFG)

    def test_quoted_unknown_and_cyclic_dependencies_block_manifest(self):
        import build_knowledge_manifest as knowledge
        from unittest.mock import patch
        for target, diagnostic in [('not_defined', 'unknown dependency'), ('customer', 'cyclic')]:
            with self.subTest(target=target):
                def altered(path):
                    meta = compiler.load_front_matter(path)
                    if path.name == 'customer.md':
                        meta['sql'] = meta['sql'].replace('{{ontology}}.revenue_order',
                                                        '`{{ontology}}` /* gap */ . `' + target + '`')
                    return meta
                with patch.object(knowledge, 'load_front_matter', side_effect=altered):
                    with self.assertRaisesRegex(ValueError, diagnostic):
                        knowledge.build_manifest()

    def test_quoted_excluded_reference_blocks_cli_before_output(self):
        import subprocess
        import yaml
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            cfg = root / 'config.yml'
            cfg.write_text(yaml.safe_dump(dict(CFG, exclude_objects=['order'])))
            driver = '''
import pathlib, sys
from unittest.mock import patch
sys.path.insert(0, 'ontology/scripts')
sys.path.insert(0, 'scripts')
import compile_ontology as compiler
import build_knowledge_manifest as knowledge
original = compiler.load_front_matter
def altered(path):
    meta = original(path)
    if path.name == 'revenue_order.md':
        meta['sql'] = meta['sql'].replace('{{ontology}}.order', '`{{ontology}}` /* gap */ . `order`')
    return meta
sys.argv = ['compile_ontology.py', '--config', sys.argv[1], '--offline-preview', '--out', sys.argv[2]]
with patch.object(compiler, 'load_front_matter', side_effect=altered), patch.object(knowledge, 'load_front_matter', side_effect=altered):
    compiler.main()
'''
            result = subprocess.run([sys.executable, '-c', driver, str(cfg), str(root/'out')],
                                    cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('dependency', result.stderr)
            self.assertFalse((root/'out').exists())
            self.assertNotIn('CREATE', result.stdout)


class SecondReviewProvenanceTests(unittest.TestCase):
    def test_offset_bounds_rejected_before_datetime_normalization(self):
        from build_knowledge_manifest import validate_provenance
        for offset in ('+00:60', '+00:99', '-00:60', '-12:99', '+24:00', '-24:00', '+99:00'):
            with self.subTest(offset=offset):
                with self.assertRaisesRegex(ValueError, 'generated_at'):
                    validate_provenance({'generated_at': '2001-01-01T00:00:00' + offset,
                                         'source_commit': '0' * 40})

    def test_historical_valid_offsets_remain_accepted(self):
        from build_knowledge_manifest import validate_provenance
        for offset in ('Z', '+00:00', '-00:00', '+05:30', '-07:00', '+23:59', '-23:59'):
            with self.subTest(offset=offset):
                validate_provenance({'generated_at': '2001-01-01T00:00:00.123' + offset,
                                     'source_commit': '0' * 40})
