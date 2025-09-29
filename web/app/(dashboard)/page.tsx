import { DashboardInsetLayout } from '@/components/layouts/dashboard/DashboardInsetLayout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function HomePage() {
  return (
    <DashboardInsetLayout title="Dashboard" className="p-4 lg:p-6">
      <Card className="@container/card">
        <CardHeader>
          <CardTitle>Welcome to Practice Hub</CardTitle>
        </CardHeader>
        <CardContent>
          <p>
            Add your goals, track your progress, and improve your musical
            skills.
          </p>
        </CardContent>
      </Card>
    </DashboardInsetLayout>
  );
}
