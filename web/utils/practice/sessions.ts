import { PracticeSession } from '@/models/practice';

export const isSessionActive = (session?: PracticeSession | null) => {
  return !!session?.started_at && !session?.stopped_at;
};
