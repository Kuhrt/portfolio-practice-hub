'use client';

import ErrorLayout from '@/components/layouts/ErrorLayout';

export default function ErrorPage({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <ErrorLayout title="Something went wrong!" error={error} reset={reset} />
  );
}
