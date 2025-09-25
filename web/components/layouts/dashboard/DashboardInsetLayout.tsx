import { PropsWithChildren } from 'react';

import { cn } from '@/utils/styles';

import { DashboardHeader } from './DashboardHeader';

interface Props extends PropsWithChildren {
  className?: string;
  title: string;
}

// * I hate that I had to do this, it has to be added to every page in the dashboard. I refuse to use parallel routes just for a title.
export function DashboardInsetLayout({ children, title, className }: Props) {
  return (
    <>
      <DashboardHeader title={title} />
      <main
        className={cn(
          '@container/main flex flex-1 flex-col gap-4 md:gap-6 *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:shadow-xs',
          className
        )}
      >
        {children}
      </main>
    </>
  );
}
