import type { Airport, RecommendationContext } from './types';
import airportsData from '../../data/airports.json';

const allAirports: Airport[] = airportsData as Airport[];

export function getAllAirports(): Airport[] {
  return [...allAirports].sort((a, b) => a.displayOrder - b.displayOrder);
}

export function getAirportBySlug(slug: string): Airport | undefined {
  return allAirports.find(a => a.slug === slug);
}

export function getAirportRecommendations(context: RecommendationContext, limit = 6): Airport[] {
  let filtered: Airport[] = [];

  switch (context) {
    case 'cheap':
      filtered = allAirports
        .filter(a => a.pricing.monthly !== null || a.pricing.annual !== null)
        .sort((a, b) => {
          const priceA = a.pricing.monthly ?? (a.pricing.annual ? a.pricing.annual / 12 : 999);
          const priceB = b.pricing.monthly ?? (b.pricing.annual ? b.pricing.annual / 12 : 999);
          return priceA - priceB;
        });
      break;

    case 'beginner':
      // Easy to use, affordable, good platform support
      filtered = allAirports
        .filter(a => (a.pricing.monthly !== null && a.pricing.monthly <= 25) || a.hasClash)
        .sort((a, b) => (a.pricing.monthly ?? 99) - (b.pricing.monthly ?? 99));
      break;

    case 'streaming':
      // Explicitly mentioned streaming services
      filtered = allAirports
        .filter(a => a.streamingServices.length > 0)
        .sort((a, b) => b.streamingServices.length - a.streamingServices.length);
      break;

    case 'ai':
      // Explicitly mentioned AI services (ChatGPT, Claude, etc.)
      filtered = allAirports
        .filter(a => a.aiServices.length > 0)
        .sort((a, b) => b.aiServices.length - a.aiServices.length);
      break;

    case 'clash':
      // Dedicated Clash support or verified multi-platform clients
      filtered = allAirports
        .filter(a => a.hasClash || a.clients.some(c => c.toLowerCase().includes('clash')))
        .sort((a, b) => a.displayOrder - b.displayOrder);
      if (filtered.length === 0) {
        filtered = getAllAirports();
      }
      break;

    case 'largeTraffic':
      // Airports with plans >= 500GB or 1TB
      filtered = allAirports.filter(a => 
        a.plans.some(p => {
          const t = p.traffic.toUpperCase();
          return t.includes('500GB') || t.includes('700GB') || t.includes('1TB') || t.includes('1.5TB') || t.includes('2TB');
        })
      );
      break;

    case 'oneTime':
      // Has one-time non-expiring traffic
      filtered = allAirports.filter(a => a.pricing.oneTime !== null);
      break;

    case 'multiDevice':
      // Explicitly supports unlimited devices
      filtered = allAirports.filter(a => 
        a.deviceLimits && (a.deviceLimits.includes('不限制') || a.deviceLimits.includes('不限'))
      );
      break;

    case 'iepl':
      filtered = allAirports.filter(a => a.architecture.toUpperCase().includes('IEPL'));
      break;

    case 'iplc':
      filtered = allAirports.filter(a => a.architecture.toUpperCase().includes('IPLC'));
      break;

    default:
      filtered = getAllAirports();
  }

  return filtered.slice(0, limit);
}

export function getRelatedAirports(currentSlug: string, limit = 4): Airport[] {
  const current = getAirportBySlug(currentSlug);
  if (!current) return getAllAirports().slice(0, limit);

  // Match by architecture, similar pricing or regions
  return allAirports
    .filter(a => a.slug !== currentSlug)
    .sort((a, b) => {
      let scoreA = 0;
      let scoreB = 0;
      if (a.architecture === current.architecture) scoreA += 2;
      if (b.architecture === current.architecture) scoreB += 2;
      const priceDiffA = Math.abs((a.pricing.monthly ?? 25) - (current.pricing.monthly ?? 25));
      const priceDiffB = Math.abs((b.pricing.monthly ?? 25) - (current.pricing.monthly ?? 25));
      return (scoreB - priceDiffB * 0.1) - (scoreA - priceDiffA * 0.1);
    })
    .slice(0, limit);
}
