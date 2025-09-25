'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Moon, Sun } from 'lucide-react';
import { useSession } from 'next-auth/react';
import { useTheme } from 'next-themes';
import * as React from 'react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { userKeys } from '@/constants/query-keys/user';
import { PracticeApi } from '@/services/api/practice';

export function ThemeModeToggle() {
  const { data: session } = useSession();
  const { setTheme } = useTheme();
  const queryClient = useQueryClient();

  const { mutate: saveTheme } = useMutation({
    mutationFn: (theme: 'light' | 'dark' | 'system') =>
      new PracticeApi({ token: session?.accessToken }).users.updateSettings({
        theme
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.currentSettings });
    }
  });

  const onThemeChange = (theme: 'light' | 'dark' | 'system') => {
    setTheme(theme);
    saveTheme(theme);
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="size-7 hover:cursor-pointer"
        >
          <Sun className="scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90" />
          <Moon className="absolute scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => onThemeChange('light')}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => onThemeChange('dark')}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => onThemeChange('system')}>
          System
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
