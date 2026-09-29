import type { Airport, RecommendationContext } from './types';
import airportsData from '../../data/airports.json';

const allAirports: Airport[] = airportsData as Airport[];

/**
 * 重点展示机场池 (Featured Airport Slugs)
 * 映射 8 家重点关注服务商：隐形人、暮光加速、飞猫云、微风网络、浪网、梯子云、灵动云、FlyV
 */
export const featuredAirportSlugs: string[] = [
  'yinxingren',    // 隐形人
  'muguang',       // 暮光加速
  'feimaoyun',     // 飞猫云
  'weifeng',       // 微风网络
  'langwang',      // 浪网
  'tiziyun',       // 梯子云
  'lingdongyun',   // 灵动云
  'flyv'           // FlyV
];

const featuredSlugSet = new Set(featuredAirportSlugs);

export function isFeaturedAirport(slug: string): boolean {
  return featuredSlugSet.has(slug);
}

export function getAllAirports(): Airport[] {
  return [...allAirports].sort((a, b) => a.displayOrder - b.displayOrder);
}

export function getAirportBySlug(slug: string): Airport | undefined {
  return allAirports.find(a => a.slug === slug);
}

/**
 * 辅助排序：优先提升重点机场曝光权重，同时保持在各条件下的确定性排序
 */
function sortByFeaturedAndPrimary<T extends Airport>(
  airports: T[],
  primaryComparator?: (a: T, b: T) => number
): T[] {
  return [...airports].sort((a, b) => {
    const aFeat = featuredSlugSet.has(a.slug);
    const bFeat = featuredSlugSet.has(b.slug);
    if (aFeat && !bFeat) return -1;
    if (!aFeat && bFeat) return 1;
    if (primaryComparator) {
      return primaryComparator(a, b);
    }
    return a.displayOrder - b.displayOrder;
  });
}

/**
 * 首页精选/热门机场推荐策略
 * 展示 6~8 家机场：其中 2~4 家来自 featuredAirportSlugs，其余按数据与展示顺序确定性补充
 */
export function getHomeFeaturedAirports(limit = 6): Airport[] {
  const all = getAllAirports();
  const featured = all.filter(a => featuredSlugSet.has(a.slug));
  const nonFeatured = all.filter(a => !featuredSlugSet.has(a.slug));

  const targetFeaturedCount = Math.min(3, featured.length);
  const targetNonFeaturedCount = limit - targetFeaturedCount;

  const selectedFeat = featured.slice(0, targetFeaturedCount);
  const selectedNonFeat = nonFeatured.slice(0, targetNonFeaturedCount);

  // 确定性交替呈现，保证展示均衡
  const result: Airport[] = [];
  const maxLen = Math.max(selectedFeat.length, selectedNonFeat.length);
  for (let i = 0; i < maxLen; i++) {
    if (i < selectedFeat.length) result.push(selectedFeat[i]);
    if (i < selectedNonFeat.length) result.push(selectedNonFeat[i]);
  }
  return result.slice(0, limit);
}

/**
 * 上下文驱动的机场推荐
 * 必须先严格满足 context 真实数据条件（如价格、流媒体、AI、专线等），在符合真实条件的子集中提升重点机场权重
 */
export function getAirportRecommendations(context: RecommendationContext, limit = 6): Airport[] {
  let filtered: Airport[] = [];

  switch (context) {
    case 'cheap':
      // 必须有公开有效月付或年付价格
      const cheapCandidates = allAirports.filter(
        a => a.pricing.monthly !== null || a.pricing.annual !== null
      );
      filtered = sortByFeaturedAndPrimary(cheapCandidates, (a, b) => {
        const priceA = a.pricing.monthly ?? (a.pricing.annual ? a.pricing.annual / 12 : 999);
        const priceB = b.pricing.monthly ?? (b.pricing.annual ? b.pricing.annual / 12 : 999);
        return priceA - priceB;
      });
      break;

    case 'beginner':
      // 必须为入门平价或有明确客户端说明
      const beginnerCandidates = allAirports.filter(
        a => (a.pricing.monthly !== null && a.pricing.monthly <= 30) || 
             a.hasClash || 
             (a.clients && a.clients.some(c => c.toLowerCase().includes('clash') || c.toLowerCase().includes('mihomo')))
      );
      filtered = sortByFeaturedAndPrimary(beginnerCandidates, (a, b) => {
        const priceA = a.pricing.monthly ?? 99;
        const priceB = b.pricing.monthly ?? 99;
        return priceA - priceB;
      });
      break;

    case 'streaming':
      // 必须有明确流媒体解锁服务记录
      const streamingCandidates = allAirports.filter(
        a => a.streamingServices && a.streamingServices.length > 0
      );
      filtered = sortByFeaturedAndPrimary(streamingCandidates, (a, b) => 
        (b.streamingServices?.length ?? 0) - (a.streamingServices?.length ?? 0)
      );
      break;

    case 'ai':
      // 必须有明确 AI (ChatGPT/Claude 等) 匹配记录
      const aiCandidates = allAirports.filter(
        a => a.aiServices && a.aiServices.length > 0
      );
      filtered = sortByFeaturedAndPrimary(aiCandidates, (a, b) => 
        (b.aiServices?.length ?? 0) - (a.aiServices?.length ?? 0)
      );
      break;

    case 'clash':
      // 必须在 source data 中明确记录支持 Clash 或 Mihomo
      const clashCandidates = allAirports.filter(
        a => a.hasClash || (a.clients && a.clients.some(c => c.toLowerCase().includes('clash') || c.toLowerCase().includes('mihomo')))
      );
      filtered = sortByFeaturedAndPrimary(clashCandidates);
      break;

    case 'largeTraffic':
      // 必须包含 500GB 以上大流量套餐计划
      const trafficCandidates = allAirports.filter(a =>
        a.plans && a.plans.some(p => {
          const t = (p.traffic || '').toUpperCase();
          return t.includes('500GB') || t.includes('700GB') || t.includes('1TB') || t.includes('1.5TB') || t.includes('2TB');
        })
      );
      filtered = sortByFeaturedAndPrimary(trafficCandidates);
      break;

    case 'oneTime':
      // 必须包含一次性不限时流量计费
      const oneTimeCandidates = allAirports.filter(a => a.pricing.oneTime !== null);
      filtered = sortByFeaturedAndPrimary(oneTimeCandidates, (a, b) => 
        (a.pricing.oneTime ?? 999) - (b.pricing.oneTime ?? 999)
      );
      break;

    case 'multiDevice':
      // 必须明确标注不限制在线客户端/设备数量
      const multiCandidates = allAirports.filter(a =>
        a.deviceLimits && (a.deviceLimits.includes('不限制') || a.deviceLimits.includes('不限'))
      );
      filtered = sortByFeaturedAndPrimary(multiCandidates);
      break;

    case 'iepl':
      // 线路架构中必须明确包含 IEPL 专线
      const ieplCandidates = allAirports.filter(a => 
        a.architecture && a.architecture.toUpperCase().includes('IEPL')
      );
      filtered = sortByFeaturedAndPrimary(ieplCandidates);
      break;

    case 'iplc':
      // 线路架构中必须明确包含 IPLC 专线
      const iplcCandidates = allAirports.filter(a => 
        a.architecture && a.architecture.toUpperCase().includes('IPLC')
      );
      filtered = sortByFeaturedAndPrimary(iplcCandidates);
      break;

    default:
      filtered = sortByFeaturedAndPrimary(getAllAirports());
  }

  return filtered.slice(0, limit);
}

export function getRelatedAirports(currentSlug: string, limit = 4): Airport[] {
  const current = getAirportBySlug(currentSlug);
  if (!current) return getAllAirports().slice(0, limit);

  return allAirports
    .filter(a => a.slug !== currentSlug)
    .sort((a, b) => {
      let scoreA = 0;
      let scoreB = 0;
      if (featuredSlugSet.has(a.slug)) scoreA += 1;
      if (featuredSlugSet.has(b.slug)) scoreB += 1;
      if (current.architecture && a.architecture === current.architecture) scoreA += 2;
      if (current.architecture && b.architecture === current.architecture) scoreB += 2;
      const priceDiffA = Math.abs((a.pricing.monthly ?? 25) - (current.pricing.monthly ?? 25));
      const priceDiffB = Math.abs((b.pricing.monthly ?? 25) - (current.pricing.monthly ?? 25));
      return (scoreB - priceDiffB * 0.1) - (scoreA - priceDiffA * 0.1);
    })
    .slice(0, limit);
}
