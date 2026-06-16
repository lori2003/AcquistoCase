// Mirror TypeScript dei modelli di output del backend.

export type ObjectiveType =
  | "near_metro"
  | "future_value"
  | "nightlife"
  | "below_market"
  | "near_center"
  | "family";

export interface ServicePreferences {
  metro: number;
  supermarket: number;
  school: number;
  bar: number;
  restaurant: number;
  park: number;
  public_transport: number;
  distance_center: number;
}

export interface PropertyInput {
  city: string;
  zone?: string | null;
  address?: string | null;
  lat?: number | null;
  lon?: number | null;
  budget_eur: number;
  price_eur: number;
  mq: number;
}

export interface EvaluationRequest {
  property: PropertyInput;
  objective: ObjectiveType;
  preferences: Partial<ServicePreferences>;
}

export interface ComponentScores {
  price_score: number;
  distance_score: number;
  services_score: number;
  objective_score: number;
}

export interface PriceContext {
  price_per_mq: number;
  omi_min_per_mq: number | null;
  omi_max_per_mq: number | null;
  delta_pct_vs_market: number | null;
  data_available: boolean;
}

export interface AmenityHit {
  category: string;
  name: string | null;
  walk_minutes: number;
  distance_m: number;
}

export interface DataRisk {
  code: string;
  message: string;
}

export interface EvaluationResponse {
  final_score: number;
  components: ComponentScores;
  coherent_with_objective: boolean;
  price_context: PriceContext;
  nearest_amenities: AmenityHit[];
  report_text: string;
  data_risks: DataRisk[];
  suggestions: string[];
}
