'use client';

import { MouseEvent } from 'react';

import { getURL } from './urls';

// https://github.com/vercel/next.js/blob/400ccf7b1c802c94127d8d8e0d5e9bdf9aab270c/packages/next/src/client/link.tsx#L169
export const isModifiedEvent = (event: MouseEvent): boolean => {
  const eventTarget = event.currentTarget as HTMLAnchorElement | SVGAElement;
  const target = eventTarget.getAttribute('target');
  return (
    (target && target !== '_self') ||
    event.metaKey ||
    event.ctrlKey ||
    event.shiftKey ||
    event.altKey || // triggers resource download
    (event.nativeEvent && event.nativeEvent.button === 1)
  );
};

export const shouldTriggerStartEvent = (
  href: string,
  clickEvent?: React.MouseEvent
) => {
  const current = window.location;
  const target = getURL(href);

  if (clickEvent && isModifiedEvent(clickEvent)) return false; // modified events: fallback to browser behavior
  if (current.origin !== target.origin) return false; // external URL
  if (current.pathname === target.pathname && current.search === target.search)
    return false; // same URL

  return true;
};
