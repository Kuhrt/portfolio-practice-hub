import { ReactNode } from 'react';

import BlankLayout from '@/components/layouts/BlankLayout';

export default function AuthLayout({ children }: { children: ReactNode }) {
  return <BlankLayout>{children}</BlankLayout>;
}
