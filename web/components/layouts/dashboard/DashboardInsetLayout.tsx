import { PropsWithChildren } from 'react';

import { cn } from '@/utils/styles';

import { DashboardHeader } from './DashboardHeader';

interface Props extends PropsWithChildren {
  className?: string;
  title: string;
}

export function DashboardInsetLayout({ children, title, className }: Props) {
  return (
    <>
      <DashboardHeader title={title} />
      <main
        className={cn(
          '@container/main flex flex-1 flex-col gap-4 py-4 md:gap-6 md:py-6',
          className
        )}
      >
        {children}
      </main>
    </>
  );
}
