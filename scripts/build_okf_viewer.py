#!/usr/bin/env python3
"""Build a self-contained OKF bundle viewer."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
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
        if ":" in line:
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


def concept_id(bundle: Path, path: Path) -> str:
    return "/" + str(path.relative_to(bundle)).replace("\\", "/")


def extract_edges(bundle: Path, path: Path, body: str, existing: set[str]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    source = concept_id(bundle, path)
    for label, target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if not clean.endswith(".md"):
            continue
        if clean.startswith("/"):
            resolved = clean
        else:
            resolved_path = (path.parent / clean).resolve()
            try:
                resolved = "/" + str(resolved_path.relative_to(bundle.resolve())).replace("\\", "/")
            except ValueError:
                continue
        if resolved in existing:
            edges.append({"source": source, "target": resolved, "label": label})
    return edges


def load_bundle(bundle: Path) -> dict[str, object]:
    docs: list[dict[str, object]] = []
    paths = sorted(
        path
        for path in bundle.rglob("*.md")
        if path.name not in {"index.md", "log.md"}
    )
    existing = {concept_id(bundle, path) for path in paths}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        docs.append(
            {
                "id": concept_id(bundle, path),
                "title": frontmatter.get("title") or path.stem,
                "type": frontmatter.get("type") or "Concept",
                "description": frontmatter.get("description") or "",
                "tags": frontmatter.get("tags") or [],
                "frontmatter": frontmatter,
                "body": body,
                "edges": extract_edges(bundle, path, body, existing),
            }
        )
    edges = [edge for doc in docs for edge in doc["edges"]]
    return {"docs": docs, "edges": edges}


def build_html(bundle_name: str, data: dict[str, object]) -> str:
    payload = json.dumps(data, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(bundle_name)} OKF Viewer</title>
<style>
:root {{
  color-scheme: light;
  --bg: #f7f8f5;
  --panel: #ffffff;
  --ink: #17211d;
  --muted: #5e6a63;
  --line: #d7ddd8;
  --accent: #25755d;
  --accent-2: #8b5d23;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background: var(--bg);
}}
header {{
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 18px;
  border-bottom: 1px solid var(--line);
  background: var(--panel);
}}
h1 {{
  font-size: 17px;
  margin: 0;
  letter-spacing: 0;
}}
main {{
  display: grid;
  grid-template-columns: minmax(260px, 360px) 1fr;
  min-height: calc(100vh - 56px);
}}
aside {{
  border-right: 1px solid var(--line);
  background: var(--panel);
  overflow: auto;
  max-height: calc(100vh - 56px);
}}
.toolbar {{
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  padding: 12px;
  border-bottom: 1px solid var(--line);
}}
input, select {{
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 10px;
  font: inherit;
  background: #fff;
}}
.list {{
  display: grid;
  gap: 1px;
}}
button.item {{
  border: 0;
  border-bottom: 1px solid #edf0ed;
  background: transparent;
  text-align: left;
  padding: 10px 12px;
  cursor: pointer;
  color: inherit;
}}
button.item:hover, button.item.active {{
  background: #eef5f1;
}}
.type {{
  display: inline-block;
  font-size: 11px;
  color: var(--accent);
  margin-bottom: 4px;
  font-weight: 700;
  text-transform: uppercase;
}}
.title {{
  font-weight: 650;
  font-size: 14px;
}}
.desc {{
  color: var(--muted);
  font-size: 12px;
  margin-top: 3px;
  line-height: 1.35;
}}
.content {{
  overflow: auto;
  max-height: calc(100vh - 56px);
  padding: 22px 28px 48px;
}}
.meta {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 8px;
  margin: 14px 0 22px;
}}
.meta div {{
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 8px 10px;
  background: var(--panel);
  font-size: 12px;
}}
pre {{
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: #111b17;
  color: #f5fff9;
  border-radius: 6px;
  padding: 14px;
}}
.body {{
  max-width: 1040px;
  line-height: 1.5;
}}
.body table {{
  border-collapse: collapse;
  width: 100%;
  font-size: 13px;
}}
.body th, .body td {{
  border: 1px solid var(--line);
  padding: 6px 8px;
  vertical-align: top;
}}
.body th {{
  background: #eef2ef;
}}
.edges {{
  color: var(--muted);
  font-size: 13px;
}}
@media (max-width: 800px) {{
  main {{ grid-template-columns: 1fr; }}
  aside {{ max-height: 42vh; border-right: 0; border-bottom: 1px solid var(--line); }}
  .content {{ max-height: none; padding: 18px; }}
}}
</style>
</head>
<body>
<header>
  <h1>{html.escape(bundle_name)} OKF Viewer</h1>
  <div id="counts" class="edges"></div>
</header>
<main>
  <aside>
    <div class="toolbar">
      <input id="search" placeholder="Search concepts">
      <select id="typeFilter"></select>
    </div>
    <div id="list" class="list"></div>
  </aside>
  <section class="content">
    <div id="detail"></div>
  </section>
</main>
<script id="bundle-data" type="application/json">{payload}</script>
<script>
const data = JSON.parse(document.getElementById('bundle-data').textContent);
const docs = data.docs;
const edges = data.edges;
let selected = docs[0]?.id;
const search = document.getElementById('search');
const typeFilter = document.getElementById('typeFilter');
const list = document.getElementById('list');
const detail = document.getElementById('detail');
document.getElementById('counts').textContent = `${{docs.length}} concepts · ${{edges.length}} links`;
const types = ['All types', ...Array.from(new Set(docs.map(d => d.type))).sort()];
typeFilter.innerHTML = types.map(t => `<option>${{escapeHtml(t)}}</option>`).join('');
search.addEventListener('input', render);
typeFilter.addEventListener('change', render);
function escapeHtml(value) {{
  return String(value ?? '').replace(/[&<>"']/g, ch => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[ch]));
}}
function markdownish(md) {{
  let text = escapeHtml(md);
  text = text.replace(/^# (.*)$/gm, '<h2>$1</h2>');
  text = text.replace(/^## (.*)$/gm, '<h3>$1</h3>');
  text = text.replace(/```sql\\n([\\s\\S]*?)```/g, '<pre>$1</pre>');
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  text = text.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<span>$1</span>');
  text = text.replace(/\\n\\|(.+)\\|\\n\\|[-:| ]+\\|\\n((?:\\|.*\\|\\n?)+)/g, tableBlock);
  text = text.replace(/\\n/g, '<br>');
  return text;
}}
function tableBlock(match, header, rows) {{
  const heads = header.split('|').map(s => s.trim()).filter(Boolean);
  const bodyRows = rows.trim().split('\\n').map(row => row.split('|').map(s => s.trim()).filter(Boolean));
  return '<table><thead><tr>' + heads.map(h => `<th>${{h}}</th>`).join('') + '</tr></thead><tbody>' +
    bodyRows.map(r => '<tr>' + r.map(c => `<td>${{c}}</td>`).join('') + '</tr>').join('') + '</tbody></table>';
}}
function filteredDocs() {{
  const q = search.value.toLowerCase();
  const type = typeFilter.value;
  return docs.filter(d => {{
    const text = `${{d.id}} ${{d.title}} ${{d.description}} ${{(d.tags || []).join(' ')}}`.toLowerCase();
    return (!q || text.includes(q)) && (type === 'All types' || d.type === type);
  }});
}}
function render() {{
  const shown = filteredDocs();
  if (!shown.find(d => d.id === selected)) selected = shown[0]?.id;
  list.innerHTML = shown.map(d => `<button class="item ${{d.id === selected ? 'active' : ''}}" data-id="${{escapeHtml(d.id)}}">
    <span class="type">${{escapeHtml(d.type)}}</span>
    <div class="title">${{escapeHtml(d.title)}}</div>
    <div class="desc">${{escapeHtml(d.description)}}</div>
  </button>`).join('');
  list.querySelectorAll('button').forEach(btn => btn.addEventListener('click', () => {{ selected = btn.dataset.id; render(); }}));
  const doc = docs.find(d => d.id === selected);
  if (!doc) {{ detail.innerHTML = '<p>No concept selected.</p>'; return; }}
  const outgoing = edges.filter(e => e.source === doc.id);
  const incoming = edges.filter(e => e.target === doc.id);
  detail.innerHTML = `<div class="type">${{escapeHtml(doc.type)}}</div>
    <h2>${{escapeHtml(doc.title)}}</h2>
    <p>${{escapeHtml(doc.description)}}</p>
    <div class="meta">
      <div><strong>Concept</strong><br>${{escapeHtml(doc.id)}}</div>
      <div><strong>Outgoing links</strong><br>${{outgoing.length}}</div>
      <div><strong>Cited by</strong><br>${{incoming.length}}</div>
      <div><strong>Tags</strong><br>${{escapeHtml((doc.tags || []).join(', '))}}</div>
    </div>
    <div class="body">${{markdownish(doc.body)}}</div>`;
}}
render();
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a static OKF viewer.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    bundle = args.bundle
    out = args.out or (bundle / "viz.html")
    data = load_bundle(bundle)
    out.write_text(build_html(bundle.name, data), encoding="utf-8")
    print(f"Wrote {out} with {len(data['docs'])} concepts and {len(data['edges'])} links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
