'use client';

import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { practiceKeys } from '@/constants/query-keys/practice';
import { PracticeApi } from '@/services/api/practice';

import SessionsTable from './SessionsTable';

export default function SessionsTableCard() {
  const { data: session } = useSession();
  const { data: sessions, isPending } = useQuery({
    queryKey: practiceKeys.sessions,
    queryFn: () =>
      new PracticeApi({ token: session?.accessToken }).sessions.getAll(),
    enabled: !!session?.accessToken
  });

  const filteredSessions =
    sessions?.filter((session) => !!session.stopped_at) ?? [];

  if (isPending)
    return <Skeleton className="h-40 w-full rounded-xl border bg-card" />;
  return (
    <Card className="@container/card">
      <CardContent className="px-4">
        <SessionsTable sessions={filteredSessions} />
      </CardContent>
    </Card>
  );
}
