import { Metadata } from 'next';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { ProgressLink } from '@/components/ui/links/progress-link';

export const metadata: Metadata = {
  title: 'Unauthorized | Practice Hub',
  description: 'You do not have permission to access this page.'
};

export default function UnauthorizedPage() {
  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>Access Denied</h1>
      </CardHeader>
      <CardContent>
        <p>
          You don&apos;t have permission to access this page. Please contact
          your administrator if you believe this is an error.
        </p>
        <Button type="button" asChild>
          <ProgressLink href="/" className="w-full mt-6">
            Return to Home
          </ProgressLink>
        </Button>
      </CardContent>
    </Card>
  );
}
