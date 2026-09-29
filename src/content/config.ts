import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    category: z.string(),
    recommendationContext: z.enum([
      'cheap',
      'beginner',
      'streaming',
      'ai',
      'clash',
      'largeTraffic',
      'oneTime',
      'multiDevice',
      'iepl',
      'iplc'
    ]).default('clash'),
    tags: z.array(z.string()).default([]),
    faq: z.array(z.object({
      q: z.string(),
      a: z.string()
    })).default([])
  })
});

export const collections = { posts };
