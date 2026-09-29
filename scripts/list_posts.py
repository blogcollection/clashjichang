import sys
from pathlib import Path
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

posts = sorted(Path('src/content/posts').glob('*.md'))
print(f"Total posts found: {len(posts)}")

cat_counts = {}
for p in posts:
    text = p.read_text(encoding='utf-8')
    cat_match = re.search(r'category:\s*["\']?([^"\'\r\n]+)', text)
    title_match = re.search(r'title:\s*["\']?([^"\'\r\n]+)', text)
    tags_match = re.search(r'tags:\s*(\[[^\]]+\])', text)
    rec_match = re.search(r'recommendationContext:\s*["\']?([^"\'\r\n]+)', text)
    cat = cat_match.group(1).strip() if cat_match else 'unknown'
    title = title_match.group(1).strip() if title_match else 'no title'
    tags = tags_match.group(1).strip() if tags_match else '[]'
    rec = rec_match.group(1).strip() if rec_match else 'none'
    cat_counts[cat] = cat_counts.get(cat, 0) + 1
    print(f"{p.stem:38} | {cat:12} | {rec:12} | {title}")

print("\nCategory counts:", cat_counts)
