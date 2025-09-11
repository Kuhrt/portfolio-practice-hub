import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader
} from '@/components/ui/card';
import { getErrorMessage } from '@/utils/errors';

interface Props {
  error?: Error & { digest?: string };
  reset?: () => void;
  title: string;
}

export default function ErrorLayout({ error, reset, title }: Props) {
  return (
    <Card className="max-w-3xl w-full">
      <CardHeader>
        <h1>{title}</h1>
      </CardHeader>
      <CardContent>{!!error && <p>{getErrorMessage(error)}</p>}</CardContent>
      {!!reset && (
        <CardFooter>
          <Button onClick={() => reset()} className="mt-6 mx-auto">
            Try again
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}
