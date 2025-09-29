'use client';

import {
  IconPlayerPlayFilled,
  IconPlayerStopFilled
} from '@tabler/icons-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { useEffect, useMemo, useState } from 'react';
import { toast } from 'sonner';

import { practiceKeys } from '@/constants/query-keys/practice';
import { useDebounce } from '@/hooks/use-debounce';
import { useTimer } from '@/hooks/use-timer';
import {
  PracticeSessionCreate,
  PracticeSessionUpdate,
  SessionType
} from '@/models/practice';
import { PracticeApi } from '@/services/api/practice';
import { getErrorMessage } from '@/utils/errors';
import { isSessionActive } from '@/utils/practice/sessions';

const descriptionId = 'practice-description';

export default function TimerBar() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const router = useRouter();
  const practiceApi = new PracticeApi({ token: session?.accessToken });

  const { data: activeSession, isPending: gettingActiveSession } = useQuery({
    queryKey: practiceKeys.activeSession,
    queryFn: () => practiceApi.sessions.getActiveSession(),
    enabled: !!session?.accessToken
  });

  const [description, setDescription] = useState(
    activeSession?.description || ''
  );
  const debouncedDescription = useDebounce(description, 500);

  const isActive = useMemo(
    () => isSessionActive(activeSession),
    [activeSession]
  );
  const elapsedTime = useTimer(activeSession?.started_at, isActive);

  const { mutate: createSession, isPending: isCreatingSession } = useMutation({
    mutationFn: (sessionData: PracticeSessionCreate) =>
      practiceApi.sessions.create(sessionData),
    onError: (error) => {
      toast.error("Couldn't create session.", {
        description: getErrorMessage(error)
      });
    },
    onSuccess: (session, initialData) => {
      queryClient.invalidateQueries({ queryKey: practiceKeys.activeSession });
      queryClient.invalidateQueries({ queryKey: practiceKeys.sessions });
      router.refresh();
      if (!initialData.description) {
        const descriptionField = document.getElementById(descriptionId);
        if (descriptionField) {
          descriptionField.focus();
        }
      }
    }
  });

  const { mutate: updateSession, isPending: isUpdatingSession } = useMutation({
    mutationFn: (data: {
      sessionId: string;
      sessionData: PracticeSessionUpdate;
    }) => practiceApi.sessions.update(data.sessionId, data.sessionData),
    onError: (error) => {
      toast.error("Couldn't update session.", {
        description: getErrorMessage(error)
      });
    },
    onSuccess: (_, { sessionId }) => {
      toast.success('Session updated.');
      queryClient.invalidateQueries({ queryKey: practiceKeys.activeSession });
      queryClient.invalidateQueries({ queryKey: practiceKeys.sessions });
      queryClient.invalidateQueries({
        queryKey: practiceKeys.session(sessionId)
      });
      router.refresh();
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

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    if (gettingActiveSession) return;
    e.preventDefault();

    if (isActive && !!activeSession) {
      endSession(activeSession.id);
    } else {
      createSession({
        session_type: SessionType.FREE_PLAY,
        description
      });
    }
  };

  const areFieldsDisabled =
    gettingActiveSession ||
    isCreatingSession ||
    isUpdatingSession ||
    isEndingSession;

  // Sync local description state with activeSession when it changes
  useEffect(() => {
    setDescription(
      activeSession?.description !== undefined ? activeSession.description : ''
    );
  }, [activeSession?.description]);

  // Debounced description update - only for active sessions
  useEffect(() => {
    if (
      isActive &&
      activeSession &&
      debouncedDescription !== activeSession.description &&
      debouncedDescription.trim() !== ''
    ) {
      // Update the session on the server
      updateSession({
        sessionId: activeSession.id,
        sessionData: { description: debouncedDescription }
      });
    }
  }, [debouncedDescription, isActive, activeSession, updateSession]);

  return (
    <form className="flex items-center gap-2 lg:gap-4" onSubmit={onSubmit}>
      <input
        type="text"
        className="flex-1 bg-transparent border-none outline-none placeholder:text-gray-500 placeholder:dark:text-gray-400  text-xl font-bold"
        placeholder="What are we practicing?"
        id={descriptionId}
        name={descriptionId}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={areFieldsDisabled}
      />
      <p className="text-xl text-gray-500 dark:text-gray-400 font-medium">
        {elapsedTime}
      </p>
      {isActive ? (
        <button
          type="submit"
          className="relative z-10 flex items-center justify-center rounded-full bg-destructive text-background p-2 hover:cursor-pointer after:content-[''] after:-z-10 after:block after:absolute after:top-1/2 after:left-1/2 after:-translate-1/2 after:rounded-full after:w-[120%] after:h-[120%] after:bg-destructive/40 after:animate-pulse"
          disabled={areFieldsDisabled}
        >
          <IconPlayerStopFilled className="size-5" />
        </button>
      ) : (
        <button
          type="submit"
          className="relative z-10 flex items-center justify-center rounded-full bg-primary text-primary-foreground p-2 hover:cursor-pointer after:content-[''] after:-z-10 after:block after:absolute after:top-1/2 after:left-1/2 after:-translate-1/2 after:rounded-full after:w-[130%] after:h-[130%] after:bg-primary/40 after:transition-all hover:after:w-[120%] hover:after:h-[120%]"
          disabled={areFieldsDisabled}
        >
          <IconPlayerPlayFilled className="size-5" />
        </button>
      )}
    </form>
  );
}
