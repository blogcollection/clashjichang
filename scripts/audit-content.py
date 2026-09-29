"""Fail the content pipeline when published posts are structurally thin or duplicated."""
from pathlib import Path
import re
import sys
from difflib import SequenceMatcher

posts = sorted(Path('src/content/posts').glob('*.md'))
failures = []
bodies = {}
paragraphs = {}

published = []
similarity_texts = {}
for path in posts:
    text = path.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    body = parts[2].strip() if len(parts) == 3 else text.strip()
    if re.search(r'^draft:\s*true\s*$', text, re.M):
        continue
    published.append(path)
    body_without_h1 = re.sub(r'^#\s+.+$', '', body, flags=re.M)
    normalized = re.sub(r'\s+', ' ', body_without_h1).strip().lower()
    normalized = re.sub(r'《[^》]+》|\(本文：[^)]+\)|（本文：[^）]+）', '', normalized)
    bodies.setdefault(normalized, []).append(path.name)
    headings = re.findall(r'^##\s+.+$', body, re.M)
    if len(headings) < 3:
        failures.append(f'{path.name}: fewer than three H2 sections')
    chunks = [re.sub(r'\s+', ' ', p).strip().lower() for p in re.split(r'\n\s*\n', body) if len(p.strip()) > 45]
    if len(chunks) < 4:
        failures.append(f'{path.name}: insufficient substantive paragraphs')
    for paragraph in chunks:
        paragraphs.setdefault(paragraph, []).append(path.name)
    comparison_body = re.sub(r'^#{1,6}\s+[^\n]+$', '', body_without_h1, flags=re.M)
    similarity_texts[path.name] = re.sub(r'\s+', ' ', re.sub(r'\*|`|\d+\.\s*', '', comparison_body)).strip().lower()

for body, names in bodies.items():
    if len(names) > 1:
        failures.append('exact duplicate body: ' + ', '.join(names))
for paragraph, names in paragraphs.items():
    if len(names) > 1:
        failures.append('duplicate substantive paragraph: ' + ', '.join(names))

scores = []
pairs_80 = []
pairs_90 = []
names = sorted(similarity_texts)
for idx, name in enumerate(names):
    for other in names[idx + 1:]:
        score = SequenceMatcher(None, similarity_texts[name], similarity_texts[other]).ratio()
        scores.append(score)
        if score >= .80: pairs_80.append((name, other, score))
        if score >= .90: pairs_90.append((name, other, score))

average = sum(scores) / len(scores) if scores else 0
maximum = max(scores) if scores else 0
print(f'Total posts: {len(posts)}; published: {len(published)}; drafts: {len(posts) - len(published)}')
print(f'Unique normalized structures: {len(set(similarity_texts.values()))}')
print(f'Normalized average similarity: {average:.3f}; max similarity: {maximum:.3f}')
print(f'Pairs >= 0.80: {len(pairs_80)}; pairs >= 0.90: {len(pairs_90)}')
if pairs_80:
    print('CONTENT_TEMPLATE_RISK')
if pairs_90:
    failures.append('multiple published articles exceed 0.90 normalized similarity')

if failures:
    print('CONTENT AUDIT FAILED')
    print('\n'.join(failures))
    sys.exit(1)
print('CONTENT AUDIT OK')
