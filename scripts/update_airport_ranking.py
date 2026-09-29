import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

target_order = [
    'yinxingren',   # 1. 隐形人
    'muguang',      # 2. 暮光加速
    'feimaoyun',    # 3. 飞猫云
    'weifeng',      # 4. 微风网络
    'langwang',     # 5. 浪网
    'tiziyun',      # 6. 梯子云
    'lingdongyun',  # 7. 灵动云
    'flyv'          # 8. FlyV
]

with open('src/data/airports.json', 'r', encoding='utf-8') as f:
    airports = json.load(f)

print(f"Total airports in database: {len(airports)}")

ordered_airports = []
used_slugs = set()

# 1. Place the 8 featured airports in exact requested order (1 to 8)
for slug in target_order:
    matched = [a for a in airports if a['slug'] == slug]
    if matched:
        ordered_airports.append(matched[0])
        used_slugs.add(slug)
    else:
        print(f"WARNING: Slug {slug} not found!")

# 2. Append the remaining airports sorted by their existing displayOrder
remaining = [a for a in airports if a['slug'] not in used_slugs]
remaining.sort(key=lambda x: x.get('displayOrder', 999))
ordered_airports.extend(remaining)

# 3. Update displayOrder 1 to 31
for idx, a in enumerate(ordered_airports, 1):
    a['displayOrder'] = idx

with open('src/data/airports.json', 'w', encoding='utf-8') as f:
    json.dump(ordered_airports, f, ensure_ascii=False, indent=2)

print("\n=== UPDATED AIRPORT ORDER (src/data/airports.json) ===")
for a in ordered_airports:
    feat_tag = "⭐ [重点推荐]" if a['slug'] in target_order else ""
    print(f"{a['displayOrder']:2d}. {a['name']:<25} ({a['slug']:<15}) {feat_tag}")
