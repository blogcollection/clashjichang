import zipfile
import xml.etree.ElementTree as ET
import json
import re
import os

def col_letter_to_index(col_str):
    num = 0
    for c in col_str:
        num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1

COUNTRY_NAMES = [
    'Hong Kong', 'Taiwan', 'Japan', 'Singapore', 'United States', 'United Kingdom',
    'Malaysia', 'Germany', 'France', 'Thailand', 'Vietnam', 'South Korea',
    'Australia', 'Canada', 'Turkey', 'Brazil', 'India', 'Indonesia', 'Philippines',
    'Russia', 'Argentina', 'Netherlands', 'Korea', 'US', 'UK', 'HK', 'JP', 'SG'
]

REGION_MAP = {
    'Hong Kong': '香港',
    'Taiwan': '台湾',
    'Japan': '日本',
    'Singapore': '新加坡',
    'United States': '美国',
    'United Kingdom': '英国',
    'Malaysia': '马来西亚',
    'Germany': '德国',
    'France': '法国',
    'Thailand': '泰国',
    'Vietnam': '越南',
    'South Korea': '韩国',
    'Korea': '韩国',
    'Australia': '澳大利亚',
    'Canada': '加拿大',
    'Turkey': '土耳其',
    'Brazil': '巴西',
    'India': '印度',
    'Indonesia': '印度尼西亚',
    'Philippines': '菲律宾',
    'Russia': '俄罗斯',
    'Argentina': '阿根廷',
    'Netherlands': '荷兰',
}

SLUG_MAP = {
    'Sogo云 (Sogo Cloud)': 'sogoyun',
    'U1S1 (有一说一)': 'u1s1',
    'Firefly 机场': 'firefly',
    'FlyV 机场': 'flyv',
    'SSONE 机场': 'ssone',
    'WgetCloud（原 GaCloud）': 'wgetcloud',
    '一翻云 (1flyun)': 'yifanyun',
    '二猫云 (2mao Cloud)': 'ermaoyun',
    '光年梯 (Guangnianti)': 'guangnianti',
    '光速云 (Lightspeed Cloud)': 'guangshuyun',
    '全球云': 'quanqiuyun',
    '可信云 (Kexin Cloud)': 'kexinyun',
    '唯兔云 (V2Yun)': 've2yun',
    '大哥云 (DeGeYun)': 'dageyun',
    '宇宙云 (Yuzhou Cloud)': 'yuzhouyun',
    '微风网络': 'weifeng',
    '快狸 (Kuaili Cloud)': 'kuaili',
    '无忧链接 (WUYOU LINK / EST. 2024)': 'wuyoulink',
    '星岛梦 (Stardream)': 'xingdaomeng',
    '暮光加速': 'muguang',
    '极连云 (Jilian Cloud)': 'jilianyun',
    '梯子云': 'tiziyun',
    '浪网': 'langwang',
    '灵动云': 'lingdongyun',
    '灵猫网络 (Spirit Cat)': 'lingmaoyun',
    '赛博云机场': 'saiboyun',
    '跨界云 (Crossover)': 'kuajieyun',
    '边缘节点 (EdgeNova)': 'edgenova',
    '速界 (Speed World)': 'sujie',
    '隐形人': 'yinxingren',
    '飞猫云': 'feimaoyun'
}

def clean_summary(text):
    if not text:
        return ""
    text = re.sub(r'^[📖\s\d大约字分钟|🏷️👁️📅\-]+(?:\|\s*)?', '', text)
    text = re.sub(r'^摘要[：:]\s*', '', text)
    return text.strip()

def clean_url(u):
    if not u:
        return None
    u = str(u).strip()
    if u.startswith('http://') or u.startswith('https://'):
        return u
    return None

def is_country_spillover(s):
    if not s:
        return True
    s_clean = s.replace('"', '').replace("'", "").strip()
    for cn in COUNTRY_NAMES:
        if s_clean.lower() == cn.lower() or f'""{cn.lower()}""' in s.lower():
            return True
    return False

def validate_device_limits(val, summary):
    if val and not is_country_spillover(val):
        s = str(val).strip()
        if any(k in s for k in ['设备', '客户端', '在线', '不限', '无限制']):
            if len(s) < 80:
                return s
    # Check if mentioned in summary
    if '不限制在线设备' in summary or '不限设备' in summary or '不限制使用客户端及设备' in summary:
        return "不限制在线设备与客户端数量"
    return None

def validate_discounts(val):
    if not val or is_country_spillover(val):
        return None
    s = str(val).strip()
    if any(k in s for k in ['折', '优惠', '满减', '立减', '专属', '%']) and len(s) < 100:
        return s
    return None

PROTOCOL_ALIASES = {
    'ss': 'Shadowsocks', 'shadowsocks': 'Shadowsocks', 'shadowsocksr': 'ShadowsocksR',
    'ssr': 'ShadowsocksR', 'v2ray': 'V2Ray', 'vmess': 'VMess', 'vless': 'VLESS',
    'trojan': 'Trojan', 'hysteria2': 'Hysteria 2', 'hysteria 2': 'Hysteria 2',
    'hy2': 'Hysteria 2', 'hysteria': 'Hysteria', 'tuic': 'TUIC', 'anytls': 'AnyTLS', 'wireguard': 'WireGuard',
}

def normalize_protocol(value):
    value = re.sub(r'^\s*(?:ss|shadowsocks)\s*\(\s*shadowsocks\s*\)\s*$', 'Shadowsocks', value, flags=re.I)
    key = re.sub(r'\s+', ' ', value.strip()).lower()
    return PROTOCOL_ALIASES.get(key, value.strip())

def parse_protocols(raw):
    """Split only explicit delimiters; whitespace is meaningful in Hysteria 2 and aliases."""
    if not raw:
        return []
    normalized_raw = re.sub(r'\bHysteria\s*2\b|\bHysteria2\b|\bHY2\b', 'Hysteria 2', raw, flags=re.I)
    normalized_raw = re.sub(r'\bSS\s*\(\s*Shadowsocks\s*\)', 'Shadowsocks', normalized_raw, flags=re.I)
    values = re.split(r'[/、,，;；\n\r]+', normalized_raw)
    result = []
    for value in values:
        protocol = normalize_protocol(re.sub(r'协议$', '', value.strip()))
        if protocol and protocol not in result and not is_country_spillover(protocol):
            result.append(protocol)
    return result

# Load XLSX
z = zipfile.ZipFile('airports.xlsx')
shared_strings = []
if 'xl/sharedStrings.xml' in z.namelist():
    tree = ET.fromstring(z.read('xl/sharedStrings.xml'))
    ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    for si in tree.findall(f'{ns}si'):
        text = ''.join(t.text or '' for t in si.findall(f'.//{ns}t'))
        shared_strings.append(text)

sheet_tree = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

matrix = []
for row in sheet_tree.findall(f'.//{ns}row'):
    row_dict = {}
    for c in row.findall(f'{ns}c'):
        ref = c.attrib.get('r', '')
        m = re.match(r'([A-Z]+)(\d+)', ref)
        if m:
            col_idx = col_letter_to_index(m.group(1))
            t = c.attrib.get('t', '')
            v_elem = c.find(f'{ns}v')
            val = v_elem.text if v_elem is not None else ''
            if t == 's' and val.isdigit():
                val = shared_strings[int(val)]
            row_dict[col_idx] = val
    matrix.append(row_dict)

headers = matrix[0]

airports = []
data_audit = {
    "totalRawRows": len(matrix) - 1,
    "successfulParsedAirports": 0,
    "anomalousAirports": 0,
    "excludedAirports": 0,
    "warningCount": 0,
    "errorCount": 0,
    "airportsWithValidPrice": 0,
    "plansJsonSuccessCount": 0,
    "plansJsonFailedCount": 0,
    "airportsWithAffiliateUrl": 0,
    "airportsWithOfficialUrl": 0,
    "airportsWithNodeRegions": 0,
    "airportsWithClashSupport": 0,
    "anomalies": [],
    "excludedList": [],
    "warnings": [],
    "errors": []
}

seen_slugs = set()

for r_idx in range(1, len(matrix)):
    r = matrix[r_idx]
    row_num = r_idx + 1

    source_file = r.get(0, '').strip()
    service_name = r.get(2, '').strip()
    aliases_raw = r.get(3, '').strip()
    summary_raw = r.get(4, '').strip()

    # Rule 3: Valid service_name check
    if not service_name or any(bad in service_name for bad in ['{', '}', '[', ']', ':"']):
        data_audit["anomalies"].append({
            "airport": service_name or f"Row_{row_num}",
            "field": "service_name",
            "rawValue": service_name,
            "problem": "invalid or corrupt service name",
            "action": "discarded row"
        })
        data_audit["anomalousAirports"] += 1
        data_audit["errorCount"] += 1
        data_audit["errors"].append(f"Row {row_num}: Invalid service name '{service_name}'")
        continue

    # Exclude row 31 (duplicate WgetCloud / 闪跃.md)
    if '闪跃' in source_file or (service_name == 'WgetCloud（原 GaCloud）' and row_num == 31):
        data_audit["excludedAirports"] += 1
        data_audit["excludedList"].append({
            "airport": service_name,
            "row": row_num,
            "sourceFile": source_file,
            "reason": "Duplicate entry under 闪跃.md with status EXCLUDED_PENDING_REVIEW",
            "action": "excluded from website"
        })
        continue

    summary_clean = clean_summary(summary_raw)

    official_url = clean_url(r.get(5, ''))
    affiliate_url = clean_url(r.get(6, ''))
    affiliate_code = r.get(7, '').strip() or None
    registration_url = clean_url(r.get(8, ''))
    telegram_url = clean_url(r.get(9, ''))
    currency = r.get(10, 'CNY').strip() or 'CNY'

    # Architecture & protocols
    arch = r.get(12, '').strip() or None
    protocols_raw = r.get(13, '').strip()
    protocols = parse_protocols(protocols_raw)

    # Reconstruct regions standardized:
    reg_start = None
    reg_end = None
    for c in range(15, 30):
        v = r.get(c, '').strip()
        if reg_start is None and v.startswith('['):
            reg_start = c
        if reg_start is not None and v.endswith(']'):
            reg_end = c
            break

    regions_list = []
    if reg_start is not None and reg_end is not None:
        raw_reg = ','.join(r.get(c, '') for c in range(reg_start, reg_end + 1)).replace('""', '"')
        try:
            arr = json.loads(raw_reg)
            if isinstance(arr, list):
                for item in arr:
                    cn = REGION_MAP.get(item, item)
                    if cn and cn not in regions_list:
                        regions_list.append(cn)
        except Exception:
            pass

    raw_regions_text = r.get(14, '').strip()
    if not regions_list and raw_regions_text:
        for en, cn in REGION_MAP.items():
            if cn in raw_regions_text or en.lower() in raw_regions_text.lower():
                if cn not in regions_list:
                    regions_list.append(cn)

    # Reconstruct plans_json
    plans_start = None
    plans_end = None
    for c in sorted(r.keys()):
        val = r[c].strip()
        if plans_start is None and (val.startswith('[{') or '[{"section"' in val):
            plans_start = c
        if plans_start is not None and (val.endswith('}]') or val.endswith('}]}]') or val.endswith('}]"}')):
            plans_end = c
            break

    plans_data = []
    if plans_start is not None and plans_end is not None:
        raw_plans_str = ','.join(r.get(c, '') for c in range(plans_start, plans_end + 1))
        for attempt in [raw_plans_str, raw_plans_str.replace('""', '"')]:
            try:
                plans_data = json.loads(attempt)
                data_audit["plansJsonSuccessCount"] += 1
                break
            except Exception:
                pass
        if not plans_data:
            data_audit["plansJsonFailedCount"] += 1
    else:
        data_audit["plansJsonFailedCount"] += 1

    formatted_plans = []
    monthly_prices = []
    annual_prices = []
    onetime_prices = []

    for section in plans_data:
        sec_name = section.get('section', '周期套餐')
        for row_item in section.get('rows', []):
            p_name = row_item.get('套餐名称') or row_item.get('套餐') or row_item.get('套餐类型') or '标准套餐'
            if ':---' in p_name or '---' in p_name:
                continue

            price_str = (row_item.get('方案价格') or row_item.get('价格') or 
                         row_item.get('基础价格') or row_item.get('基础月付') or 
                         row_item.get('订阅价格明细') or row_item.get('一次性价格') or '')
            if ':---' in price_str or price_str == ':---':
                continue

            traffic_str = (row_item.get('包含流量') or row_item.get('月流量') or 
                           row_item.get('流量') or row_item.get('周期流量') or 
                           row_item.get('套餐流量') or row_item.get('总流量') or 
                           row_item.get('月流量配额') or '详见套餐')
            if ':---' in traffic_str or traffic_str == ':-:':
                traffic_str = '以官网为准'

            cycle_str = (row_item.get('计费周期') or row_item.get('付费周期') or 
                         row_item.get('周期优惠折扣') or row_item.get('周期与折扣优惠') or '')
            
            target_user = (row_item.get('适合人群与特点') or row_item.get('适合人群') or 
                           row_item.get('适用场景') or row_item.get('特点与适用场景') or 
                           row_item.get('特点') or row_item.get('核心特点与线路包含') or '')
            if ':---' in target_user or target_user == '""':
                target_user = ''

            # Extract numeric price specifically from price_str
            num_price = None
            price_m = re.search(r'¥?\s*(\d+(?:\.\d+)?)', price_str)
            if price_m:
                try:
                    num_price = float(price_m.group(1))
                except ValueError:
                    num_price = None

            # Categorize prices
            is_onetime_sec = any(k in sec_name for k in ['一次性', '不限时'])
            is_onetime_plan = any(k in p_name for k in ['一次性', '不限时', '流量包'])
            if is_onetime_sec or is_onetime_plan:
                if num_price is not None and num_price >= 5: # avoid 1x multipliers
                    onetime_prices.append(num_price)
                if not cycle_str:
                    cycle_str = '一次性不限时'
            else:
                y_match = re.search(r'¥?\s*(\d+(?:\.\d+)?)\s*(?:元)?\s*/\s*年', price_str)
                if y_match:
                    annual_prices.append(float(y_match.group(1)))
                    if not cycle_str:
                        cycle_str = '年付'
                else:
                    m_match = re.search(r'¥?\s*(\d+(?:\.\d+)?)\s*(?:元)?\s*/\s*月', price_str)
                    if m_match:
                        monthly_prices.append(float(m_match.group(1)))
                        if not cycle_str:
                            cycle_str = '月付'

            formatted_plans.append({
                "section": sec_name,
                "name": p_name,
                "price": price_str,
                "numericPrice": num_price,
                "billingCycle": cycle_str or '标准周期',
                "traffic": traffic_str,
                "targetUser": target_user
            })

    # Strict pricing
    final_monthly = min(monthly_prices) if monthly_prices else None
    final_annual = min(annual_prices) if annual_prices else None
    final_onetime = min(onetime_prices) if onetime_prices else None

    # Fallback to pricing columns ONLY if numeric and not corrupted
    def safe_column_number(col_val):
        if not col_val or is_country_spillover(col_val):
            return None
        s = str(col_val).strip()
        if re.fullmatch(r'^\d+(\.\d+)?$', s):
            val = float(s)
            return val if val > 0 else None
        return None

    if final_monthly is None:
        final_monthly = safe_column_number(r.get(27, ''))
    if final_annual is None:
        final_annual = safe_column_number(r.get(28, ''))
    if final_onetime is None:
        final_onetime = safe_column_number(r.get(29, ''))

    if final_monthly is not None or final_annual is not None or final_onetime is not None:
        data_audit["airportsWithValidPrice"] += 1

    # CTA
    cta_url = affiliate_url or registration_url or official_url
    if not cta_url:
        cta_url = f"https://clashjichang.sbs/airports/{SLUG_MAP.get(service_name, 'airport')}/"
        cta_text = "查看详情"
    else:
        if affiliate_url:
            cta_text = "查看套餐"
        elif registration_url:
            cta_text = "访问官网"
        else:
            cta_text = "查看机场"

    if affiliate_url:
        data_audit["airportsWithAffiliateUrl"] += 1
    if official_url:
        data_audit["airportsWithOfficialUrl"] += 1
    if regions_list:
        data_audit["airportsWithNodeRegions"] += 1

    # Clients & Platforms
    clients_raw = r.get(18, '').strip()
    if is_country_spillover(clients_raw):
        clients_raw = ""
    platforms_raw = r.get(19, '').strip()
    if is_country_spillover(platforms_raw):
        platforms_raw = ""

    combined_client_text = f"{clients_raw} {platforms_raw} {summary_raw} {protocols_raw}"
    client_evidence = combined_client_text.lower()
    has_clash = any(term in client_evidence for term in ['clash', 'clash verge', 'clash meta', 'mihomo', '兼容 clash', 'clash 订阅'])
    if has_clash:
        data_audit["airportsWithClashSupport"] += 1

    supported_clients = []
    for client_name in ['Clash Verge Rev', 'Clash Meta', 'Mihomo Party', 'Clash', 'Shadowrocket', 'Sing-box', 'Surge', 'V2Ray']:
        if client_name.lower() in combined_client_text.lower():
            if client_name not in supported_clients:
                supported_clients.append(client_name)

    supported_platforms = []
    for plat in ['Windows', 'macOS', 'Android', 'iOS', 'Linux']:
        if plat.lower() in combined_client_text.lower():
            if plat not in supported_platforms:
                supported_platforms.append(plat)

    # Streaming & AI
    streaming_raw = r.get(25, '').strip()
    if is_country_spillover(streaming_raw):
        streaming_raw = ""
    ai_raw = r.get(26, '').strip()
    if is_country_spillover(ai_raw):
        ai_raw = ""
    unlock_raw = r.get(24, '').strip()
    if is_country_spillover(unlock_raw):
        unlock_raw = ""

    combined_unlock_text = f"{streaming_raw} {ai_raw} {unlock_raw} {summary_raw}"

    streaming_services = []
    for s in ['Netflix', 'Disney+', 'YouTube', 'HBO', 'TikTok', 'Hulu', 'BBC iPlayer', 'DAZN', 'Abema', 'TVer']:
        if s.lower() in combined_unlock_text.lower():
            if s not in streaming_services:
                streaming_services.append(s)

    ai_services = []
    for a in ['ChatGPT', 'Claude', 'Gemini', 'Midjourney', 'Meta AI', 'Grok']:
        if a.lower() in combined_unlock_text.lower():
            if a not in ai_services:
                ai_services.append(a)

    # Clean device limits and discounts
    device_limits = validate_device_limits(r.get(17, ''), summary_clean)
    discounts = validate_discounts(r.get(23, ''))

    # Payment methods
    payment_raw = r.get(20, '').strip()
    if is_country_spillover(payment_raw):
        payment_raw = ""
    payment_methods = []
    for pm in ['支付宝', '微信支付', 'USDT', '信用卡', '虚拟币']:
        if pm in payment_raw or pm in summary_raw:
            payment_methods.append(pm)

    # Features
    features = []
    if plans_end is not None:
        trailing_cols = [r.get(c, '').strip() for c in range(plans_end + 1, max(r.keys()) + 1) if r.get(c, '').strip()]
        for text_chunk in trailing_cols:
            if ' | ' in text_chunk and len(text_chunk) > 40:
                bullets = [b.strip() for b in text_chunk.split(' | ') if b.strip()]
                for b in bullets:
                    if b not in features and len(b) > 5 and not b.startswith('http') and not is_country_spillover(b):
                        features.append(b)

    slug = SLUG_MAP.get(service_name)
    if not slug:
        slug = re.sub(r'[^a-zA-Z0-9]+', '', service_name).lower() or f"airport-{row_num}"
    if slug in seen_slugs:
        slug = f"{slug}-{row_num}"
    seen_slugs.add(slug)

    aliases = [a.strip() for a in re.split(r'[/,，、\s]+', aliases_raw) if a.strip() and not is_country_spillover(a)]

    airport_obj = {
        "id": f"ap_{row_num:02d}",
        "slug": slug,
        "name": service_name,
        "aliases": aliases,
        "summary": summary_clean,
        "officialUrl": official_url,
        "affiliateUrl": affiliate_url,
        "registrationUrl": registration_url,
        "telegramUrl": telegram_url,
        "ctaUrl": cta_url,
        "ctaText": cta_text,
        "currency": currency,
        "architecture": arch,
        "protocols": protocols,
        "regions": regions_list or None,
        "deviceLimits": device_limits,
        "clients": supported_clients,
        "platforms": supported_platforms,
        "hasClash": has_clash,
        "paymentMethods": payment_methods,
        "discounts": discounts,
        "streamingServices": streaming_services,
        "aiServices": ai_services,
        "pricing": {
            "monthly": final_monthly,
            "annual": final_annual,
            "oneTime": final_onetime
        },
        "plans": formatted_plans,
        "features": features[:6],
        "verification": {
            "status": "服务商资料整理",
            "level": "资料参考",
            "isIndependentVerified": False,
            "note": "以上线路、协议、解锁与性能描述整理自现有服务资料；本站未进行统一独立性能测试，实际情况请以当前服务页面及个人网络环境测试为准。"
        },
        "lastChecked": "2026-09-28",
        "displayOrder": row_num
    }

    airports.append(airport_obj)
    data_audit["successfulParsedAirports"] += 1

with open('src/data/airports.json', 'w', encoding='utf-8') as f:
    json.dump(airports, f, ensure_ascii=False, indent=2)

with open('src/data/data-audit.json', 'w', encoding='utf-8') as f:
    json.dump(data_audit, f, ensure_ascii=False, indent=2)

print("Regenerated airports.json and data-audit.json successfully!")
print(f"Total active airports: {len(airports)}")
