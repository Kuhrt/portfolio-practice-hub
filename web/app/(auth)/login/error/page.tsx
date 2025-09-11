'use client';

import { useSearchParams } from 'next/navigation';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { ProgressLink } from '@/components/ui/links/progress-link';

export default function LoginErrorPage() {
  const searchParams = useSearchParams();
  const error = searchParams.get('error');

  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>Authentication Error</h1>
      </CardHeader>
      <CardContent>
        <p>
          {!!error
            ? `The following error has occurred: ${error}`
            : 'An unknown error has occurred.'}
        </p>
        <Button type="button" asChild>
          <ProgressLink href="/" className="w-full mt-4">
            Go home
          </ProgressLink>
        </Button>
      </CardContent>
    </Card>
  );
}
