export interface FeedItem {
  id: string;
  url: string;
  title: string;
  source: string;
  raw_text: string;
  summary?: string;
  category?: string;
  sentiment?: string;
  entities_json?: {
    companies: string[];
    robots: string[];
    people: string[];
    technologies: string[];
  };
  relevance_score?: number;
  enriched: boolean;
  created_at: string;
  enriched_at?: string;
}

export interface TrendingData {
  companies: [string, number][];
  technologies: [string, number][];
}

export interface StatusData {
  counts: Record<string, number>;
  unenriched: number;
  last_scraped: Record<string, string | null>;
  timestamp?: string;
}
