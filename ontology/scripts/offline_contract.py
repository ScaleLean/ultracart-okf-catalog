"""Dataset-specific historical schema checks. No warehouse or semantic attestation."""
import pathlib
import re
from sql_syntax import classify_source

CURRENT_DATASETS = {'ultracart_dw', 'ultracart_dw_low', 'ultracart_dw_medium', 'ultracart_dw_high'}
DATASETS = {'dw': 'ultracart_dw', 'low': 'ultracart_dw_low',
            'medium': 'ultracart_dw_medium', 'high': 'ultracart_dw_high'}
TYPE_ALIASES = {'INT64': 'INTEGER', 'BOOL': 'BOOLEAN', 'FLOAT64': 'FLOAT'}
SQL_KEYWORDS = set('''case when then else end and or not in is null true false coalesce array_length
concat cast safe_cast date datetime timestamp string integer int64 numeric boolean bool current_date
current_datetime current_timestamp date_sub date_diff date_trunc interval day month year to_hex
 to_base64 from_hex safe from_base64 lower upper trim sha256 if ifnull nullif count countif sum min
max avg row_number over partition by order group select from where left join on using as distinct
unnest struct array like between extract safe_divide regexp_contains split array_to_string exists'''.split())


def column_refs(expr):
    expr = re.sub(r"'[^']*'", '', expr)
    return {t for t in re.findall(r'\b[A-Za-z_][A-Za-z0-9_.]*\b', expr)
            if t.split('.')[0].lower() not in SQL_KEYWORDS}


def schema_for(root, dataset, table):
    path = pathlib.Path(root) / 'tables' / dataset / (table + '.md')
    if not path.exists():
        return None
    return dict(re.findall(r'^\| `([A-Za-z0-9_.]+)` \| `([^`]+)` \|', path.read_text(), re.MULTILINE))


def normalized_type(value):
    return TYPE_ALIASES.get(value.upper(), value.upper())


def binding_parts(meta, cfg):
    if cfg.get('bindings'):
        raise ValueError('binding overrides unsupported offline: scope, grain and expression types cannot be attested')
    template = meta['source']['default_table']
    match = re.fullmatch(r'\{\{source_project\}\}\.\{\{dataset\.(\w+)\}\}\.([A-Za-z0-9_]+)', template)
    if not match:
        raise ValueError('unsupported source binding syntax')
    tier, table = match.groups()
    if tier not in cfg.get('dataset', {}):
        raise ValueError(f'explicit dataset selection required for {tier}')
    dataset = cfg['dataset'][tier]
    if dataset not in CURRENT_DATASETS:
        raise ValueError(f'unsupported dataset {dataset}: current-state grain/scope unavailable offline')
    return dataset, table


def check_binding(meta, cfg, root):
    errors = []
    if not meta.get('grain') or not meta.get('key', {}).get('fields'):
        errors.append('missing declared grain/key (uniqueness remains unverified)')
    try:
        dataset, table = binding_parts(meta, cfg)
    except (KeyError, ValueError) as e:
        return errors + [str(e)]
    schema = schema_for(root, dataset, table)
    if schema is None:
        return errors + [f'no dataset-specific schema for {dataset}.{table}']
    # Compare expression operands to their historical default schema, never to a union.
    default_tier = re.search(r'dataset\.(\w+)', meta['source']['default_table']).group(1)
    baseline = schema_for(root, DATASETS.get(default_tier, ''), table) or {}
    unnest = meta['source'].get('unnest')
    def resolve(ref):
        if unnest and ref.startswith(unnest['alias'] + '.'):
            return unnest['field'] + ref[len(unnest['alias']):]
        return ref
    if unnest and not schema.get(unnest['field'], '').startswith('ARRAY<'):
        errors.append(f'unnest field {unnest["field"]} missing or not ARRAY')
    props = meta.get('properties', [])
    names = [p.get('name') for p in props]
    if len(set(names)) != len(names):
        errors.append('duplicate property names')
    for key in meta.get('key', {}).get('fields', []):
        if key not in names:
            errors.append(f'key {key} not an output property')
    for prop in props:
        if not prop.get('name') or not prop.get('type') or not prop.get('source'):
            errors.append('missing property name/type/source')
            continue
        source = prop['source']
        try:
            direct = classify_source(source)
        except ValueError as e:
            errors.append(f'{prop["name"]}: {e}')
            continue
        direct_field = direct is not None
        refs = set(prop.get('refs') or ({direct} if direct_field else column_refs(source)))
        if direct_field:
            refs.add(direct)
        for ref in refs:
            ref = resolve(ref)
            if ref not in schema:
                errors.append(f'{prop["name"]}: required field {ref} missing in {dataset}.{table}')
            elif ref in baseline and normalized_type(schema[ref]) != normalized_type(baseline[ref]):
                errors.append(f'{prop["name"]}: source type mismatch for {ref}: {schema[ref]} vs {baseline[ref]}')
        if direct_field:
            ref = resolve(direct)
            if ref in schema and normalized_type(schema[ref]) != normalized_type(prop['type']):
                errors.append(f'{prop["name"]}: output type mismatch: {schema[ref]} vs {prop["type"]}')
    merchant_filter = meta['source'].get('merchant_filter')
    if merchant_filter:
        if merchant_filter != "merchant_id = '{{merchant_id}}'":
            errors.append('unsupported merchant scope filter')
        if normalized_type(schema.get('merchant_id', 'UNKNOWN')) != 'STRING':
            errors.append('merchant scope requires STRING merchant_id in selected dataset')
    # An absent filter is not proof of a single-merchant source. The manifest records it
    # as unresolved; deployable compilation is refused for all offline-only contracts.
    return errors
