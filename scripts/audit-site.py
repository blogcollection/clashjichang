import os
import re
import xml.etree.ElementTree as ET

dist_dir = 'dist'

all_html_files = []
for root, dirs, files in os.walk(dist_dir):
    for f in files:
        if f.endswith('.html'):
            all_html_files.append(os.path.join(root, f))

print(f"Total HTML files in dist: {len(all_html_files)}")

# Collect all routes generated
routes = set()
for hf in all_html_files:
    rel = os.path.relpath(hf, dist_dir).replace('\\', '/')
    if rel == 'index.html':
        route = '/'
    elif rel.endswith('/index.html'):
        route = '/' + rel[:-10]
    else:
        route = '/' + rel
    routes.add(route)

titles = {}
descriptions = {}
broken_links = []
prohibited_findings = []
missing_canonical = []
empty_pages = []

DISALLOWED = ['localhost', '127.0.0.1', 'example.com', 'example.org', 'NaN', 'undefined', '[object Object]', '{"section":']

for hf in all_html_files:
    rel_path = os.path.relpath(hf, dist_dir).replace('\\', '/')
    size = os.path.getsize(hf)
    if size < 200:
        empty_pages.append((rel_path, size))

    with open(hf, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check disallowed terms in visible html (ignoring standard js script attributes if any)
    for bad in DISALLOWED:
        if bad in html:
            prohibited_findings.append((rel_path, bad))

    # Regex checks for title and meta
    title_m = re.search(r'<title>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else None
    if title:
        titles.setdefault(title, []).append(rel_path)
    else:
        prohibited_findings.append((rel_path, 'missing <title>'))

    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.DOTALL | re.IGNORECASE)
    if not desc_m:
        desc_m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.DOTALL | re.IGNORECASE)
    desc = desc_m.group(1).strip() if desc_m else None
    if desc:
        descriptions.setdefault(desc, []).append(rel_path)
    else:
        prohibited_findings.append((rel_path, 'missing <meta description>'))

    can_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](https://clashjichang\.sbs.*?)["\']', html, re.IGNORECASE)
    if not can_m:
        missing_canonical.append(rel_path)

    # Check internal links
    hrefs = re.findall(r'href=["\'](/.*?)["\']', html)
    for href in hrefs:
        # Strip query and hash
        clean_href = href.split('?')[0].split('#')[0]
        if not clean_href or clean_href == '/':
            continue
        # Ensure trailing slash normalized
        check_path = clean_href if clean_href.endswith('/') else clean_href + '/'
        
        # Check if corresponding file exists
        target_file = os.path.join(dist_dir, check_path.lstrip('/').replace('/', os.sep), 'index.html')
        target_direct = os.path.join(dist_dir, clean_href.lstrip('/').replace('/', os.sep))
        if not os.path.exists(target_file) and not os.path.exists(target_direct):
            broken_links.append((rel_path, href))

# Duplicate titles
duplicate_titles = {t: paths for t, paths in titles.items() if len(paths) > 1}
# Duplicate descriptions
duplicate_descriptions = {d: paths for d, paths in descriptions.items() if len(paths) > 1}

# Check sitemap
sitemap_files = [f for f in os.listdir(dist_dir) if f.startswith('sitemap') and f.endswith('.xml')]
sitemap_urls = set()
for sf in sitemap_files:
    tree = ET.parse(os.path.join(dist_dir, sf))
    root = tree.getroot()
    # check if sitemapindex or urlset
    for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        sitemap_urls.add(elem.text)

# Check robots.txt
robots_txt_exists = os.path.exists(os.path.join(dist_dir, 'robots.txt'))

print("\n=== AUDIT RESULTS ===")
print(f"Total HTML pages: {len(all_html_files)}")
print(f"Sitemap XML files found: {sitemap_files}")
print(f"Total Sitemap URLs indexed: {len(sitemap_urls)}")
print(f"robots.txt exists: {robots_txt_exists}")
print(f"Empty pages (<200 bytes): {len(empty_pages)}")
print(f"Missing canonical links: {len(missing_canonical)}")
print(f"Broken internal links: {len(broken_links)}")
print(f"Prohibited tokens found (localhost/NaN/etc): {len(prohibited_findings)}")
print(f"Duplicate titles: {len(duplicate_titles)}")
print(f"Duplicate descriptions: {len(duplicate_descriptions)}")

if broken_links:
    print("\nSample broken links (first 10):")
    for r, h in broken_links[:10]:
        print(f"  {r} -> {h}")

if prohibited_findings:
    print("\nSample prohibited tokens:")
    for r, b in prohibited_findings[:10]:
        print(f"  {r}: {b}")

if duplicate_titles:
    print("\nSample duplicate titles:")
    for t, p in list(duplicate_titles.items())[:5]:
        print(f"  Title: '{t}' in {p}")
