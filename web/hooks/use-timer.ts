import { DateTime } from 'luxon';
import { useEffect, useState } from 'react';

/**
 * Custom hook for running a timer based on a start time
 * @param startTime - The start time as an ISO string
 * @param isActive - Whether the timer should be running
 * @returns The formatted elapsed time as HH:MM:SS
 */
export function useTimer(
  startTime: string | null | undefined,
  isActive: boolean
): string {
  const [elapsedTime, setElapsedTime] = useState('0:00:00');

  useEffect(() => {
    if (!isActive || !startTime) {
      setElapsedTime('0:00:00');
      return;
    }

    const start = DateTime.fromISO(startTime, { zone: 'utc' });
    const updateTimer = () => {
      const now = DateTime.utc();
      const elapsed = now.diff(start);

      const formattedTime = elapsed.toFormat('hh:mm:ss');
      setElapsedTime(formattedTime);
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [startTime, isActive]);

  return elapsedTime;
}
