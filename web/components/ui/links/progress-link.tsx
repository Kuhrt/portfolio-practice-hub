'use client';

import NextLink, { LinkProps } from 'next/link';
import nProgress from 'nprogress';

import { shouldTriggerStartEvent } from '@/utils/events';
import { cn } from '@/utils/styles';

//This component should be used instead of Link to make nProgress work
export const ProgressLink = (
  props: Omit<
    React.AnchorHTMLAttributes<HTMLAnchorElement>,
    keyof LinkProps<unknown>
  > &
    LinkProps<unknown> & {
      children?: React.ReactNode | undefined;
    } & React.RefAttributes<HTMLAnchorElement>
) => {
  const { className, href, onClick, ...restProps } = props;
  const targetHref = typeof href === 'string' ? href : href.pathname;

  return (
    <NextLink
      href={href}
      onClick={(event) => {
        if (shouldTriggerStartEvent(targetHref ?? '', event)) {
          nProgress.start();
        }
        if (!!onClick) {
          onClick(event);
        }
      }}
      className={cn('hover:cursor-pointer', className)}
      {...restProps}
    />
  );
};

ProgressLink.displayName = 'ProgressLink';
