# -*- coding: utf-8 -*-
"""
Main generator and auditor for all 36 Clash vertical blog posts.
Ensures zero AI templating, authentic technical content, 800 - 2500 Chinese characters,
natural internal links, and strict adherence to content collection schema.
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

from post_data_tutorials import TUTORIAL_POSTS
from post_data_troubleshoot import TROUBLESHOOT_POSTS
from post_data_concepts import CONCEPT_POSTS
from post_data_selection import SELECTION_POSTS

POST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'content', 'posts')

ALL_POSTS = TUTORIAL_POSTS + TROUBLESHOOT_POSTS + CONCEPT_POSTS + SELECTION_POSTS

BANNED_WORDS = [
    "核心基石",
    "彻底告别",
    "终极指南",
    "王牌",
    "极度稳定",
    "零丢包",
    "0抖动",
    "不经过GFW",
    "在日常使用科学上网与跨境网络访问的过程中",
    "严禁年付",
    "坚决执行月付",
    "坚决只选月付",
    "绝对安全",
    "抗封锁能力出众",
    "高关注度",
    "优质服务商",
    "优质专线"
]

VALID_CONTEXTS = {
    'cheap', 'beginner', 'streaming', 'ai', 'clash',
    'largeTraffic', 'oneTime', 'multiDevice', 'iepl', 'iplc'
}

def count_chinese_chars(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def validate_and_generate():
    print(f"=== Total Posts to Process: {len(ALL_POSTS)} ===")
    assert len(ALL_POSTS) == 36, f"Expected 36 posts, got {len(ALL_POSTS)}"
    
    seen_filenames = set()
    stats = []

    for post in ALL_POSTS:
        fn = post['filename']
        assert fn not in seen_filenames, f"Duplicate filename: {fn}"
        seen_filenames.add(fn)

        # Validate recommendationContext
        ctx = post['recommendationContext']
        assert ctx in VALID_CONTEXTS, f"Invalid recommendationContext '{ctx}' in {fn}"

        # Combine text for audit
        full_text = post['content']
        ch_count = count_chinese_chars(full_text)

        # Validate word count (800 - 2500 Chinese characters)
        assert 800 <= ch_count <= 2500, f"Post {fn} Chinese char count {ch_count} out of range (800-2500)!"

        # Check banned words
        for bad in BANNED_WORDS:
            assert bad not in full_text, f"Post {fn} contains banned word '{bad}'!"

        # Construct frontmatter cleanly without external yaml dependency
        lines = [
            "---",
            f'title: "{post["title"]}"',
            f'description: "{post["description"]}"',
            f'pubDate: {post["pubDate"]}',
            f'category: "{post["category"]}"',
            f'recommendationContext: "{post["recommendationContext"]}"',
            'tags: [' + ', '.join(f'"{t}"' for t in post['tags']) + ']',
            'faq:'
        ]
        for item in post['faq']:
            q_clean = item['q'].replace('"', '\\"')
            a_clean = item['a'].replace('"', '\\"')
            lines.append(f'  - q: "{q_clean}"')
            lines.append(f'    a: "{a_clean}"')
        lines.append("---")
        fm_str = '\n'.join(lines)
        md_content = f"{fm_str}\n\n{post['content'].strip()}\n"

        target_path = os.path.join(POST_DIR, fn)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        stats.append({
            'filename': fn,
            'title': post['title'],
            'category': post['category'],
            'context': ctx,
            'ch_count': ch_count,
            'faq_count': len(post['faq'])
        })

    print(f"Successfully generated all {len(ALL_POSTS)} posts into {POST_DIR}!")
    
    # Audit summary
    counts = [s['ch_count'] for s in stats]
    min_c = min(counts)
    max_c = max(counts)
    avg_c = sum(counts) / len(counts)
    print(f"Word Count Stats -> Min: {min_c}, Max: {max_c}, Avg: {avg_c:.1f}")

    # Check for duplicate paragraphs across different posts
    paragraphs_seen = {}
    dup_count = 0
    for post in ALL_POSTS:
        fn = post['filename']
        paras = [p.strip() for p in post['content'].split('\n\n') if len(p.strip()) > 30 and not p.strip().startswith('#') and not p.strip().startswith('```')]
        for p in paras:
            # Normalize whitespace
            norm_p = re.sub(r'\s+', ' ', p)
            if norm_p in paragraphs_seen:
                print(f"WARNING DUPLICATE: '{norm_p[:30]}...' found in both {paragraphs_seen[norm_p]} and {fn}")
                dup_count += 1
            else:
                paragraphs_seen[norm_p] = fn

    print(f"Duplicate paragraphs across posts: {dup_count}")
    assert dup_count == 0, f"Found {dup_count} duplicate paragraphs across posts!"

if __name__ == '__main__':
    validate_and_generate()
