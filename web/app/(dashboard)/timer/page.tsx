import { DashboardInsetLayout } from '@/components/layouts/dashboard/DashboardInsetLayout';
import TimerBar from '@/components/practice/TimerBar';
import { Card, CardContent } from '@/components/ui/card';

const practiceHeadlines = [
  "Practice? We talkin' about practice?",
  '10,000 hours? More like 10,000 excuses!',
  "Practice makes perfect? I'm still waiting...",
  'Another day, another scale to butcher!',
  "Metronome? I don't need no stinking metronome!",
  "Practice until your fingers bleed... or until dinner's ready",
  "Perfect practice makes perfect? I'll settle for 'not terrible'",
  'Practice is like vegetables - good for you but nobody wants to do it',
  'I practice in my sleep... that counts, right?',
  'Practice makes permanent... hopefully not permanently bad!'
];

export default function TimerPage() {
  const headlineIndex = Math.floor(Math.random() * practiceHeadlines.length);
  const headline = practiceHeadlines[headlineIndex];

  return (
    <DashboardInsetLayout title={headline} className="p-4 lg:p-6">
      <Card className="@container/card">
        <CardContent className="px-4">
          <TimerBar />
        </CardContent>
      </Card>
    </DashboardInsetLayout>
  );
}
