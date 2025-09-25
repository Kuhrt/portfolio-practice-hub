export interface PracticeSessionCreate {
  user_id?: string;
  description?: string;
  session_type: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export interface PracticeSessionUpdate {
  description?: string;
  started_at?: string;
  stopped_at?: string;
  session_type?: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export interface PracticeSession {
  id: string;
  description?: string;
  started_at: string;
  stopped_at: string;
  duration: number;
  session_type: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export enum SessionType {
  EXERCISE = 'exercise',
  FREE_PLAY = 'free_play',
  SONG = 'song',
  STRUCTURED = 'structured',
  TECHNIQUE = 'technique'
}
