'use client';

import { isServer, QueryClientProvider } from '@tanstack/react-query';
import { Session } from 'next-auth';
import { SessionProvider } from 'next-auth/react';
import { PropsWithChildren } from 'react';

import { getQueryClient } from '@/utils/queries';

import { ThemeProvider } from './ThemeProvider';

interface Props extends PropsWithChildren {
  refetchInterval?: number;
  session?: Session;
}

export default function Providers({ children, refetchInterval = 0 }: Props) {
  const queryClient = getQueryClient(isServer);

  return (
    <SessionProvider refetchInterval={refetchInterval}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </QueryClientProvider>
    </SessionProvider>
  );
}
