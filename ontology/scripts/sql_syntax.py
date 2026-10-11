"""Limited offline SQL tokens and normalization, not a SQL semantic verifier.

Positions permit rewriting only parsed ontology references. Unsupported lexical
forms and ambiguous source shapes fail closed; reviewed derived shapes remain
explicitly unverified, rather than being called direct-field validation.
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    start: int
    end: int


def tokenize(sql):
    tokens, i = [], 0
    while i < len(sql):
        start = i
        if sql[i].isspace():
            i += 1
            continue
        if sql.startswith('--', i):
            end = sql.find('\n', i)
            i = len(sql) if end < 0 else end + 1
            continue
        if sql.startswith('/*', i):
            end = sql.find('*/', i + 2)
            if end < 0 or '/*' in sql[i + 2:end]:
                raise ValueError('unsupported or unterminated SQL comment')
            i = end + 2
            continue
        if sql[i] in "'\"`":
            quote = sql[i]
            i += 1
            value = []
            while i < len(sql):
                if sql[i] == quote:
                    if i + 1 < len(sql) and sql[i + 1] == quote:
                        if quote == '`':
                            raise ValueError('unsupported escaped identifier')
                        value.append(quote)
                        i += 2
                        continue
                    i += 1
                    break
                if sql[i] == '\\':
                    if quote == '`' or i + 1 >= len(sql):
                        raise ValueError('unsupported escaped identifier/string')
                    value.append(sql[i:i + 2])
                    i += 2
                    continue
                value.append(sql[i])
                i += 1
            else:
                raise ValueError('unterminated SQL quote')
            tokens.append(Token('quoted' if quote == '`' else 'string', ''.join(value), start, i))
            continue
        if sql.startswith('{{', i):
            end = sql.find('}}', i + 2)
            if end < 0:
                raise ValueError('unterminated SQL template')
            i = end + 2
            tokens.append(Token('template', sql[start:i], start, i))
            continue
        match = re.match(r'[A-Za-z_][A-Za-z0-9_]*|[0-9]+(?:\.[0-9]+)?', sql[i:])
        if match:
            value = match.group()
            i += len(value)
            tokens.append(Token('number' if value[0].isdigit() else 'word', value, start, i))
            continue
        if sql[i] not in '().,[]=<>+-*/!|:%;@$':
            raise ValueError('unsupported SQL token')
        i += 1
        tokens.append(Token('symbol', sql[start:i], start, i))
    return tokens


def _balanced(tokens):
    stack = []
    for token in tokens:
        if token.kind == 'symbol' and token.value in ('(', '['):
            stack.append(token.value)
        elif token.kind == 'symbol' and token.value in (')', ']'):
            if not stack or stack.pop() != {')': '(', ']': '['}[token.value]:
                raise ValueError('unbalanced source parentheses/brackets')
    if stack:
        raise ValueError('unbalanced source parentheses/brackets')


def _identifier(token):
    if token.kind not in ('word', 'quoted') or not re.fullmatch(
            r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', token.value):
        raise ValueError('unsupported direct-field identifier')
    return token.value


DERIVED_FUNCTIONS = {'array_length', 'coalesce', 'concat', 'date', 'date_diff', 'safe_cast'}
DERIVED_OPERATORS = {'+', '-', '*', '/', '=', '<', '>', '!', 'and', 'or', 'in', 'is', 'between', 'like'}


def classify_source(expr):
    """Return a normalized direct field, or None for reviewed derived/literal shapes.

    Field paths permit comments/whitespace, quoted components or whole paths, and
    redundant parentheses. Other shapes must be recognizable derived expressions;
    this classification does not infer derived types or verify their full grammar.
    """
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError('empty source expression')
    _balanced(tokens)
    while tokens[0].value == '(' and tokens[-1].value == ')':
        depth, wraps_all = 0, True
        for i, token in enumerate(tokens):
            if token.value == '(':
                depth += 1
            elif token.value == ')':
                depth -= 1
            if depth == 0 and i != len(tokens) - 1:
                wraps_all = False
                break
        if not wraps_all:
            break
        tokens = tokens[1:-1]
        if not tokens:
            raise ValueError('empty parenthesized source')
    if len(tokens) == 1 and (tokens[0].kind in ('number', 'string') or
                            tokens[0].kind == 'word' and tokens[0].value.lower() in {'true', 'false', 'null'}):
        return None

    def path_at(index):
        if tokens[index].value == '(':
            path, index = path_at(index + 1)
            if index >= len(tokens) or tokens[index].value != ')':
                raise ValueError('not a direct path')
            index += 1
        else:
            path, index = _identifier(tokens[index]), index + 1
        while index < len(tokens) and tokens[index].value == '.':
            if index + 1 >= len(tokens):
                raise ValueError('incomplete direct path')
            path += '.' + _identifier(tokens[index + 1])
            index += 2
        return path, index

    try:
        path, end = path_at(0)
        if end == len(tokens):
            return path
    except (ValueError, IndexError):
        pass
    if any(token.value in ('[', ']', ';', '@', '$') for token in tokens):
        raise ValueError('unsupported source expression shape')
    head = tokens[0].value.lower()
    if head in {'select', 'case', 'not'} or (
            head in DERIVED_FUNCTIONS and len(tokens) > 1 and tokens[1].value == '('):
        return None
    # Binary arithmetic/predicates are derived declarations, never direct-field proof.
    if any(token.kind != 'string' and token.value.lower() in DERIVED_OPERATORS for token in tokens):
        return None
    raise ValueError('unclassified source expression; direct validation refused')


@dataclass(frozen=True)
class OntologyReference:
    name: str
    start: int
    end: int


def ontology_references(sql):
    """Parse every active ontology template into a tracked object/view reference.

    Support bare paths, fully backticked paths and individually/partially quoted
    components, with comments/whitespace between components. No table decorators,
    extra path components or dynamic lookups. Literals/comments are not references.
    """
    tokens, refs, i = tokenize(sql), [], 0
    while i < len(tokens):
        token = tokens[i]
        if token.kind == 'string' and '{{' in token.value and 'ontology' in token.value:
            previous = tokens[i - 1] if i else None
            following = tokens[i + 1] if i + 1 < len(tokens) else None
            if (previous and (previous.kind == 'word' and previous.value.lower() in {'from', 'join'} or
                              previous.kind == 'symbol' and previous.value == '.')) or (
                    following and following.kind == 'symbol' and following.value == '.'):
                raise ValueError('unsupported ontology reference: string quoting is not identifier quoting')
        active = token.kind in ('template', 'quoted') and 'ontology' in token.value and '{{' in token.value
        if not active:
            i += 1
            continue
        if i and (tokens[i - 1].kind == 'symbol' and tokens[i - 1].value == '.' or
                  tokens[i - 1].end == token.start and tokens[i - 1].kind in ('word', 'quoted', 'template', 'string')):
            raise ValueError('unsupported ontology reference prefix')
        name, end_index = None, i
        if token.kind == 'quoted':
            match = re.fullmatch(r'\{\{ontology\}\}\.([A-Za-z_][A-Za-z0-9_]*)', token.value)
            if match:
                name = match.group(1)
            elif token.value != '{{ontology}}':
                raise ValueError('unsupported quoted ontology reference grammar')
        elif token.value != '{{ontology}}':
            raise ValueError('unsupported ontology reference template')
        if name is None:
            if i + 2 >= len(tokens) or tokens[i + 1].value != '.' or tokens[i + 1].kind != 'symbol':
                raise ValueError('unsupported ontology reference: expected dataset.object')
            target = tokens[i + 2]
            if target.kind not in ('word', 'quoted') or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', target.value):
                raise ValueError('unsupported ontology reference object identifier')
            name, end_index = target.value, i + 2
        if end_index + 1 < len(tokens):
            following = tokens[end_index + 1]
            if following.value in ('.', '[', '(', '@', '$') or (
                    following.start == tokens[end_index].end and following.kind in ('word', 'quoted', 'template', 'string')):
                raise ValueError('unsupported ontology reference suffix')
        refs.append(OntologyReference(name, token.start, tokens[end_index].end))
        i = end_index + 1
    return refs


def ontology_dependencies(sql):
    return sorted({ref.name for ref in ontology_references(sql)})


def rewrite_ontology_references(sql, ontology):
    """Rewrite the exact spans used by dependency extraction, leaving literals intact."""
    pieces, cursor = [], 0
    for ref in ontology_references(sql):
        pieces.extend((sql[cursor:ref.start], f'`{ontology}.{ref.name}`'))
        cursor = ref.end
    pieces.append(sql[cursor:])
    return ''.join(pieces)
