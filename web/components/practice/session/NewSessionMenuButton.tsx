'use client';

import {
  IconCirclePlusFilled,
  IconClockFilled,
  IconPlayerStopFilled
} from '@tabler/icons-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { usePathname, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { toast } from 'sonner';

import { SidebarMenuButton } from '@/components/ui/sidebar';
import { ROUTES } from '@/constants/navigation';
import { practiceKeys } from '@/constants/query-keys/practice';
import { useTimer } from '@/hooks/use-timer';
import { PracticeSessionCreate, SessionType } from '@/models/practice';
import { PracticeApi } from '@/services/api/practice';
import { getErrorMessage } from '@/utils/errors';
import { isSessionActive } from '@/utils/practice/sessions';

export default function NewSessionMenuButton() {
  const pathname = usePathname();
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const router = useRouter();
  const practiceApi = new PracticeApi({ token: session?.accessToken });

  const { data: activeSession, isPending: gettingActiveSession } = useQuery({
    queryKey: practiceKeys.activeSession,
    queryFn: () => practiceApi.sessions.getActiveSession(),
    enabled: !!session?.accessToken
  });

  const isActive = isSessionActive(activeSession);
  const elapsedTime = useTimer(activeSession?.started_at, isActive);

  const { mutate: createSession, isPending: isCreatingSession } = useMutation({
    mutationFn: (sessionData: PracticeSessionCreate) =>
      practiceApi.sessions.create(sessionData),
    onError: (error) => {
      toast.error("Couldn't create session.", {
        description: getErrorMessage(error)
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: practiceKeys.activeSession });
      queryClient.invalidateQueries({ queryKey: practiceKeys.sessions });
      router.refresh();
      router.push(ROUTES.SESSIONS);
    }
  });

  const { mutate: endSession, isPending: isEndingSession } = useMutation({
    mutationFn: (sessionId: string) => practiceApi.sessions.end(sessionId),
    onError: (error) => {
      toast.error("Couldn't end session.", {
        description: getErrorMessage(error)
      });
    },
    onSuccess: (_, sessionId) => {
      toast.success('Session ended.');
      queryClient.invalidateQueries({ queryKey: practiceKeys.activeSession });
      queryClient.invalidateQueries({ queryKey: practiceKeys.sessions });
      queryClient.invalidateQueries({
        queryKey: practiceKeys.session(sessionId)
      });
      router.refresh();
    }
  });

  const onClick = () => {
    if (isActive && !!activeSession) {
      endSession(activeSession?.id);
    } else {
      createSession({ session_type: SessionType.FREE_PLAY });
    }
  };

  const isDisabled =
    gettingActiveSession || isCreatingSession || isEndingSession;

  return (
    <SidebarMenuButton
      tooltip="Start Session"
      disabled={isDisabled}
      onClick={onClick}
      className={`bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground min-w-8 duration-200 ease-linear overflow-hidden ${isActive ? 'animate-pulse' : ''} ${pathname === ROUTES.SESSIONS ? 'h-0 p-0 opacity-0' : ''}`}
    >
      {isActive ? (
        <>
          <IconClockFilled />
          <span className="font-medium">{elapsedTime}</span>
          <IconPlayerStopFilled className="ms-auto" />
        </>
      ) : (
        <>
          <IconCirclePlusFilled />
          <span>Start Session</span>
        </>
      )}
    </SidebarMenuButton>
  );
}
