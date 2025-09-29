import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from '@/components/ui/sidebar';
import { NavItem } from '@/models/navigation/NavItem';

import NewSessionMenuButton from '../practice/session/NewSessionMenuButton';
import { ProgressLink } from '../ui/links/progress-link';

interface Props {
  items: NavItem[];
}

export default function NavMain({ items }: Props) {
  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <nav aria-label="Main navigation">
          <SidebarMenu>
            <SidebarMenuItem className="flex items-center gap-2">
              <NewSessionMenuButton />
            </SidebarMenuItem>
            {items.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton
                  tooltip={item.title}
                  isActive={item.isActive}
                  asChild
                >
                  <ProgressLink href={item.url}>
                    {item.icon && <item.icon />}
                    <span>{item.title}</span>
                  </ProgressLink>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </nav>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
