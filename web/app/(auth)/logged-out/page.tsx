import { Card, CardContent, CardHeader } from '@/components/ui/card';

export default function LoggedOutPage() {
  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>Logged Out</h1>
      </CardHeader>
      <CardContent>
        <p>You may now close this window.</p>
      </CardContent>
    </Card>
  );
}
