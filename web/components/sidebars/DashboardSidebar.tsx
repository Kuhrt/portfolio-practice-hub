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
      url: '/',
      icon: IconLayoutDashboard,
      isActive: pathname === '/'
    },
    {
      title: 'Sessions',
      url: '/timer',
      icon: IconVinyl,
      isActive: pathname === '/timer'
    },
    {
      title: 'Goals',
      url: '/goals',
      icon: IconPennant,
      isActive: pathname === '/goals'
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
              <ProgressLink href="#">
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
