import sys
import re
import urllib.request
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFYING TUTORIALS PAGE (HTTP 200) ===")
req = urllib.request.urlopen('http://localhost:8989/tutorials/')
status = req.status
html = req.read().decode('utf-8')
print(f"Status Code: {status}")

# Count articles
article_matches = re.findall(r'<article[^>]*>[\s\S]*?</article>', html)
print(f"Total Article Cards on /tutorials/: {len(article_matches)}")

# Check H2 categories
h2s = re.findall(r'<h2[^>]*>([\s\S]*?)</h2>', html)
cleaned_h2s = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s]
print("Categories / H2 Sections:")
for idx, h in enumerate(cleaned_h2s):
    print(f"  [{idx+1}] {h}")

# Check Airport Cards in top section
top_cards = re.findall(r'href="/airports/([^/]+)/"', html[:html.find('主流客户端安装与实操教程')])
print(f"Top Airport Cards count: {len(top_cards)} ({top_cards})")

# Check Airport Cards in middle section
mid_section = html[html.find('常用 Clash 机场推荐'):html.find('节点选择与底层专线知识')]
mid_cards = re.findall(r'href="/airports/([^/]+)/"', mid_section)
print(f"Middle Airport Cards count: {len(mid_cards)} ({mid_cards})")

# Check Bottom Section Action Buttons
bottom_section = html[html.find('不知道选哪个机场？'):]
has_airports_btn = '/airports/' in bottom_section
has_recommend_btn = '/recommend/' in bottom_section
has_compare_btn = '/compare/' in bottom_section
print(f"Bottom 3 Action Buttons Present: airports={has_airports_btn}, recommend={has_recommend_btn}, compare={has_compare_btn}")

print("\n=== VERIFYING 3 RANDOM POSTS VIA HTTP ===")
sample_posts = [
    '/posts/windows-clash-tutorial/',
    '/posts/how-to-import-clash-subscription/',
    '/posts/what-is-iplc-node/'
]

for sp in sample_posts:
    r = urllib.request.urlopen(f'http://localhost:8989{sp}')
    p_html = r.read().decode('utf-8')
    title_match = re.search(r'<h1[^>]*>([\s\S]*?)</h1>', p_html)
    p_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else 'Unknown'
    has_guide = '配置好 Clash 后，你需要一个稳定的机场订阅' in p_html
    airport_links = re.findall(r'href="/airports/([^/]+)/"', p_html)
    unique_airports = list(dict.fromkeys(airport_links))
    print(f"[{r.status}] {sp} | Title: {p_title[:28]}... | Has Rec Banner: {has_guide} | Rec Airports: {unique_airports[:3]}")

print("\n=== VERIFYING 100% AIRPORT REC COVERAGE ON ALL 36 POSTS ===")
post_files = sorted(Path('dist/posts').glob('*/index.html'))
print(f"Total post HTML files built: {len(post_files)}")
covered = 0
for pf in post_files:
    text = pf.read_text(encoding='utf-8')
    if '配置好 Clash 后，你需要一个稳定的机场订阅' in text and '/airports/' in text:
        covered += 1
    else:
        print(f"MISSING REC: {pf}")

print(f"Total Article Coverage: {covered} / {len(post_files)} ({covered/len(post_files)*100:.1f}%)")
