import './globals.css';

import type { Metadata } from 'next';
import { Noto_Sans, Noto_Sans_Mono } from 'next/font/google';
import { Suspense } from 'react';

import Providers from '@/components/providers/Providers';
import AppProgressBar from '@/components/ui/progress/app-progress-bar';
import { NProgressDone } from '@/components/ui/progress/nprogress-done';

const fontSans = Noto_Sans({
  variable: '--font-noto-sans',
  subsets: ['latin']
});

const fontMono = Noto_Sans_Mono({
  variable: '--font-noto-mono',
  subsets: ['latin']
});

export const metadata: Metadata = {
  title: 'Practice Hub',
  description:
    'Add your goals, track your progress, and improve your musical skills.'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${fontSans.variable} ${fontMono.variable} antialiased`}
      suppressHydrationWarning
    >
      <body>
        <AppProgressBar />
        <Providers>{children}</Providers>
        <Suspense fallback={null}>
          <NProgressDone />
        </Suspense>
      </body>
    </html>
  );
}
