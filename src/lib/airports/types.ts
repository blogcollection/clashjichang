export interface AirportPlan {
  section?: string;
  name: string;
  price: string;
  numericPrice: number | null;
  billingCycle: string;
  traffic: string;
  targetUser?: string;
  buyUrl?: string;
}

export interface AirportVerification {
  status: string;
  level: string;
  isIndependentVerified: boolean;
  note: string;
}

export interface AirportPricing {
  monthly: number | null;
  annual: number | null;
  oneTime: number | null;
}

export interface Airport {
  id: string;
  slug: string;
  name: string;
  aliases: string[];
  summary: string;

  officialUrl: string | null;
  affiliateUrl: string | null;
  registrationUrl: string | null;
  telegramUrl: string | null;
  ctaUrl: string;
  ctaText: string;

  currency: string;

  architecture: string;
  protocols: string[];

  regions: string[];

  deviceLimits: string | null;
  clients: string[];
  platforms: string[];
  hasClash: boolean;

  paymentMethods: string[];
  discounts: string | null;

  streamingServices: string[];
  aiServices: string[];

  pricing: AirportPricing;
  plans: AirportPlan[];

  features: string[];
  verification: AirportVerification;
  lastChecked: string;
  displayOrder: number;
}

export type RecommendationContext = 
  | 'cheap'
  | 'beginner'
  | 'streaming'
  | 'ai'
  | 'clash'
  | 'largeTraffic'
  | 'oneTime'
  | 'multiDevice'
  | 'iepl'
  | 'iplc';
