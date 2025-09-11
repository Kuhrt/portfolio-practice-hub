'use client';

import { redirect, useSearchParams } from 'next/navigation';
import { signIn, useSession } from 'next-auth/react';
import nProgress from 'nprogress';
import { useEffect } from 'react';

import { Card, CardContent, CardHeader } from '@/components/ui/card';

export default function LoginPage() {
  const searchParams = useSearchParams();
  const { data: session, status } = useSession();

  useEffect(() => {
    const next = searchParams.get('next');
    const error = searchParams.get('error');

    if (!!error) {
      redirect(`/login/error?error=${error}`);
    } else if (status === 'unauthenticated' || !!session?.tokenError) {
      nProgress.start();
      void signIn('keycloak', { redirectTo: next ?? undefined });
    } else {
      const nextUrl = next;
      redirect(nextUrl ?? '/');
    }
  }, [searchParams, session, status]);

  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>Login</h1>
      </CardHeader>
      <CardContent>
        <p>You are being logged in...</p>
      </CardContent>
    </Card>
  );
}
