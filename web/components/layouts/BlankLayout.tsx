import { ReactNode } from 'react';

export default function BlankLayout({ children }: { children: ReactNode }) {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-4 bg-linear-to-tl from-primary/30 to-muted/30 p-6">
      {children}
    </main>
  );
}
