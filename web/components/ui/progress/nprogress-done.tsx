'use client';

import { usePathname, useSearchParams } from 'next/navigation';
import nProgress from 'nprogress';
import { useEffect } from 'react';

export function NProgressDone() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  useEffect(() => {
    if (nProgress.isStarted()) {
      nProgress.done(true);
    }
  }, [pathname, searchParams]);
  return null;
}
