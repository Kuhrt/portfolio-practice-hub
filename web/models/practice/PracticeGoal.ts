import { PracticeSession } from './PracticeSession';

export interface PracticeGoalCreate {
  title: string;
  description: string;
  target_date?: string;
  priority?: number;
  target: number;
  target_type: PracticeTargetType;
  target_interval: PracticeInterval;
  instrument?: string;
}

export interface PracticeGoalUpdate {
  title?: string;
  description?: string;
  status?: GoalStatus;
  is_active?: boolean;
  target_date?: string;
  priority?: number;
  target?: number;
  target_type?: PracticeTargetType;
  target_interval?: PracticeInterval;
  instrument?: string;
}

export interface PracticeGoal {
  id: string;
  title: string;
  description: string;
  status: GoalStatus;
  is_active: boolean;
  target_date?: string;
  priority: number;
  target: number;
  target_type: PracticeTargetType;
  target_interval: PracticeInterval;
  instrument?: string;
  sessions?: PracticeSession[];
}

export enum GoalStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  PAUSED = 'paused',
  CANCELLED = 'cancelled'
}

export enum PracticeTargetType {
  MINUTES = 'minutes',
  SESSIONS = 'sessions',
  REPETITIONS = 'repetitions'
}

export enum PracticeInterval {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  YEARLY = 'yearly'
}
