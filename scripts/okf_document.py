"""Shared safe YAML support for OKF 0.2. No network access."""
from __future__ import annotations

import re
from datetime import datetime, timezone
import yaml

class Loader(yaml.SafeLoader):
    """Keep ISO timestamps as authored strings."""

Loader.yaml_implicit_resolvers = {
    key: [(tag, rule) for tag, rule in values if tag != 'tag:yaml.org,2002:timestamp']
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def parse(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z', text, re.S)
    if not match:
        return None
    try:
        data = yaml.load(match[1], Loader=Loader)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data, match[2]


def serialize(frontmatter, body=''):
    return '---\n' + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip() + '\n---\n\n' + body.lstrip('\n')


def upgrade(frontmatter, body, actor):
    """Migrate recorded evidence without inventing verification or freshness."""
    fm = dict(frontmatter)
    if 'timestamp' in fm:
        stamp = fm.pop('timestamp')
        fm.setdefault('generated', {'by': actor, 'at': stamp})
    if 'okf_version' in fm:
        fm['okf_version'] = '0.2'
    match = re.search(r'^# Citations\s*\n(.*?)(?=^# |\Z)', body, re.M | re.S)
    if match:
        sources = list(fm.get('sources', []))
        for line in match[1].splitlines():
            if not line.strip():
                continue
            link = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            resource = link[2] if link else re.sub(r'^\s*(?:\[\d+\]|[-*])\s*', '', line)
            source = {'resource': resource}
            if link:
                source['title'] = link[1]
            if source not in sources:
                sources.append(source)
        fm['sources'] = sources
        body = body[:match.start()] + body[match.end():]
    return fm, body


def verified_events(fm):
    value = fm.get('verified', [])
    return [value] if isinstance(value, dict) else value if isinstance(value, list) else []


def trust_tier(fm):
    events = verified_events(fm)
    if any(str(e.get('by', '')).startswith('human:') for e in events if isinstance(e, dict)):
        return 'human-reviewed'
    return 'machine-confirmed' if events else 'unverified'


def is_stale(fm, now=None):
    try:
        value = str(fm.get('stale_after', ''))
        if 'T' not in value:
            return False
        instant = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return instant.tzinfo is not None and (now or datetime.now(timezone.utc)) >= instant
    except ValueError:
        return False
