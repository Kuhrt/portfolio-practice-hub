import { Metadata } from 'next';

import ErrorLayout from '@/components/layouts/ErrorLayout';

// TODO: Metadata doesn't actually work yet. It will need to be updated once Vercel has solved: https://github.com/vercel/next.js/issues/45620
export const metadata: Metadata = {
  title: '404 | Practice Hub'
};

export default function NotFound() {
  return (
    <ErrorLayout
      title="404 - Page not found"
      error={new Error("Sorry! We can't find what you're looking for.")}
    />
  );
}
