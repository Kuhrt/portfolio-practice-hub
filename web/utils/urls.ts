import { addBasePath } from 'next/dist/client/add-base-path';

export const getURL = (href: string) => {
  return new URL(addBasePath(href), location.href);
};
