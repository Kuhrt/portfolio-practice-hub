import { DashboardInsetLayout } from '@/components/layouts/dashboard/DashboardInsetLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function GoalsPage() {
  return (
    <DashboardInsetLayout title="Goals" className="p-4 lg:p-6">
      <Card className="@container/card">
        <CardHeader>
          <CardTitle>We are lazy</CardTitle>
        </CardHeader>
        <CardContent>
          <p>No goals for us yet. Working on it!</p>
        </CardContent>
      </Card>
    </DashboardInsetLayout>
  );
}
