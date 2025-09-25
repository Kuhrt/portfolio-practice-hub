'use client';

import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import * as React from 'react';

import { userKeys } from '@/constants/query-keys/user';
import { PracticeApi } from '@/services/api/practice';

export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  const { defaultTheme, ...restProps } = props;
  const { data: session } = useSession();

  const { data: userSettings } = useQuery({
    queryKey: userKeys.currentSettings,
    queryFn: () =>
      new PracticeApi({ token: session?.accessToken }).users.getSettings(),
    enabled: !!session?.accessToken
  });

  return (
    <NextThemesProvider
      defaultTheme={userSettings?.theme || defaultTheme}
      {...restProps}
    >
      {children}
    </NextThemesProvider>
  );
}
