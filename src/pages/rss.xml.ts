import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const posts = (await getCollection('posts')).filter(post => !post.data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());

  const itemsXml = sortedPosts.map(post => `
    <item>
      <title><![CDATA[${post.data.title}]]></title>
      <link>https://clashjichang.sbs/posts/${post.slug}/</link>
      <guid>https://clashjichang.sbs/posts/${post.slug}/</guid>
      <description><![CDATA[${post.data.description}]]></description>
      <pubDate>${post.data.pubDate.toUTCString()}</pubDate>
    </item>
  `).join('');

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Clash机场</title>
    <link>https://clashjichang.sbs</link>
    <description>Clash机场推荐、节点测速筛选、订阅教程与客户端故障排查知识库</description>
    <language>zh-CN</language>
    <atom:link href="https://clashjichang.sbs/rss.xml" rel="self" type="application/rss+xml"/>
    ${itemsXml}
  </channel>
</rss>`;

  return new Response(rss, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8'
    }
  });
};
