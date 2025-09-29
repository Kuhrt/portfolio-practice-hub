import { PracticeGoal } from '../practice';

export interface UserProfile {
  id: string;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  display_name?: string;
  timezone: string;
  last_login?: string;
  created_at: string;
}

export interface UserProfileUpdate {
  display_name?: string;
  timezone?: string;
}

export interface UserSettings {
  default_session_type?: string;
  preferred_tempo_range_min?: number;
  preferred_tempo_range_max?: number;
  default_difficulty_level?: number;
  daily_practice_goal_minutes: number;
  weekly_practice_goal_sessions: number;
  theme: string;
  profile_public: boolean;
  share_practice_stats: boolean;
  updated_at?: string;
}

export interface UserSettingsUpdate {
  default_session_type?: string;
  preferred_tempo_range_min?: number;
  preferred_tempo_range_max?: number;
  default_difficulty_level?: number;
  daily_practice_goal_minutes?: number;
  weekly_practice_goal_sessions?: number;
  theme?: string;
  profile_public?: boolean;
  share_practice_stats?: boolean;
}

export interface UserWithSettings {
  profile: UserProfile;
  settings: UserSettings;
}

export interface UserGoals {
  practice_goals: PracticeGoal[];
}
