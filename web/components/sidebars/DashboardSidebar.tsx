'use client';

import {
  IconLayoutDashboard,
  IconMusicHeart,
  IconPennant,
  IconVinyl
} from '@tabler/icons-react';
import { usePathname } from 'next/navigation';

import { ProgressLink } from '@/components/ui/links/progress-link';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from '@/components/ui/sidebar';
import { ROUTES } from '@/constants/navigation';
import { NavItem } from '@/models/navigation/NavItem';

import NavMain from '../navigation/NavMain';
import { NavUser } from '../navigation/NavUser';

export function DashboardSidebar({
  ...props
}: React.ComponentProps<typeof Sidebar>) {
  const pathname = usePathname();
  const items: NavItem[] = [
    {
      title: 'Dashboard',
      url: ROUTES.HOME,
      icon: IconLayoutDashboard,
      isActive: pathname === ROUTES.HOME
    },
    {
      title: 'Sessions',
      url: ROUTES.SESSIONS,
      icon: IconVinyl,
      isActive: pathname === ROUTES.SESSIONS
    },
    {
      title: 'Goals',
      url: ROUTES.GOALS,
      icon: IconPennant,
      isActive: pathname === ROUTES.GOALS
    }
  ];

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <ProgressLink href={ROUTES.HOME}>
                <IconMusicHeart className="!size-5 text-primary" />
                <span className="text-base font-semibold">Practice Hub</span>
              </ProgressLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={items} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser />
      </SidebarFooter>
    </Sidebar>
  );
}
