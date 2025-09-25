export const practiceKeys = {
  activeSession: ['active-session'] as const,
  sessions: ['sessions'] as const,
  session: (id: string) => [...practiceKeys.sessions, id] as const
};
