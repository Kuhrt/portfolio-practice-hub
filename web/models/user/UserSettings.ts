export interface UserSettings {
  daily_practice_goal_minutes: number;
  default_difficulty_level?: number;
  default_session_type?: string;
  preferred_tempo_range_max?: number;
  preferred_tempo_range_min?: number;
  profile_public: boolean;
  share_practice_stats: boolean;
  theme: string;
  updated_at?: string;
  weekly_practice_goal_sessions: number;
}
