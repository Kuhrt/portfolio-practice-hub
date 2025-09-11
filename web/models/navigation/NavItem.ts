import { type Icon } from '@tabler/icons-react';

export interface NavItem {
  title: string;
  icon: Icon;
  url: string;
  active?: boolean;
}
