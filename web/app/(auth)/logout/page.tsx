'use client';

import { signOut } from 'next-auth/react';
import nProgress from 'nprogress';
import { useEffect } from 'react';

import { Card, CardContent, CardHeader } from '@/components/ui/card';

export default function LogoutPage() {
  useEffect(() => {
    const logout = async () => {
      nProgress.start();
      await signOut({ redirectTo: '/logged-out' });
    };

    logout();
  }, []);

  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>Logging Out</h1>
      </CardHeader>
      <CardContent>
        <p>You are being logged out...</p>
      </CardContent>
    </Card>
  );
}
