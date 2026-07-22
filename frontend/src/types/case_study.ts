// frontend/src/types/case_study.ts

export interface CaseStudy {
  id: string;
  title: string;
  category: string;
  status: string;
  event_date: string;
  location: string;
  cause: string;
  affected: number;
}

export interface TimelineEvent {
  id: string;
  event_timestamp: string;
  responsible_actor: string;
  description: string;
}

export interface LegalReference {
  id: string;
  ref_type: string;
  title: string;
  description: string;
}

export interface MediaItem {
  id: string;
  type: string;
  source_attribution: string;
  url: string;
}

export interface HistoricalOutcome {
  immediate_actions: string[];
  committees_formed: string[];
  final_reforms: string[];
  after_effects: string[];
}

// Matches the backend's aggregated GET /api/v1/case-studies/{id} response
export interface CaseStudyResponse {
  case_study: CaseStudy;
  timeline_events: TimelineEvent[];
  legal_references: LegalReference[];
  media_items: MediaItem[];
  historical_outcome: HistoricalOutcome | null;
}

export interface SubmissionPayload {
  case_study_id: string;
  user_id: string;
  own_analysis: string;
  immediate_action: string[];
  problem_highlights: string[];
  constitutional_refs: string[];
  policy_reforms: string[];
}

export interface ProsConsAnalysis {
  pros: string[];
  cons: string[];
  additions: string[];
  deletions: string[];
}

export interface CritiqueResponse {
  submission_id: string;
  summary_of_user_idea: string;
  future_prediction: string;
  pros_cons_additions_deletions: ProsConsAnalysis;
  reality_comparison: string | null;
  created_at: string;
}