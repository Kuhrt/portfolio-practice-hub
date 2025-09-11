export interface PracticeSessionCreate {
  started_at?: string;
  session_type: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export interface PracticeSessionUpdate {
  started_at?: string;
  ended_at?: string;
  session_type?: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export interface PracticeSession {
  id: string;
  started_at: string;
  ended_at: string;
  session_type: SessionType;
  tempo?: number;
  difficulty_level?: number;
  notes?: string;
  instrument?: string;
  rating?: number;
}

export enum SessionType {
  PRACTICE = 'practice',
  REHEARSAL = 'rehearsal',
  PERFORMANCE = 'performance',
  LESSON = 'lesson'
}
