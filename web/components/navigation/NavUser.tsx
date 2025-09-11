'use client';

import {
  IconCreditCard,
  IconDotsVertical,
  IconLogout,
  IconNotification,
  IconUserCircle
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { SidebarMenuButton, useSidebar } from '@/components/ui/sidebar';
import { userKeys } from '@/constants/query-keys/user';
import { PracticeApi } from '@/services/api/practice';

import { ProgressLink } from '../ui/links/progress-link';
import { Skeleton } from '../ui/skeleton';
import { UserAvatar } from '../user/UserAvatar';

export function NavUser() {
  const { data: session } = useSession();
  const { isMobile } = useSidebar();
  const api = new PracticeApi({ token: session?.accessToken });

  const { data: userProfile, isPending: isProfilePending } = useQuery({
    queryKey: userKeys.currentProfile,
    queryFn: () => api.users.getProfile(),
    enabled: !!session?.accessToken
  });

  const fullName = !!userProfile
    ? userProfile.first_name + ' ' + userProfile.last_name
    : '';

  if (!isProfilePending && !userProfile) return null;
  return isProfilePending ? (
    <Skeleton className="h-12 w-full rounded-lg" />
  ) : (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <SidebarMenuButton
          size="lg"
          className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
        >
          {!!userProfile && (
            <UserAvatar user={userProfile} className="grayscale" />
          )}
          <div className="grid flex-1 text-left text-sm leading-tight">
            <span className="truncate font-medium">
              {fullName ?? userProfile.username}
            </span>
            <span className="text-muted-foreground truncate text-xs">
              {userProfile.email}
            </span>
          </div>
          <IconDotsVertical className="ml-auto size-4" />
        </SidebarMenuButton>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
        side={isMobile ? 'bottom' : 'right'}
        align="end"
        sideOffset={4}
      >
        <DropdownMenuLabel className="p-0 font-normal">
          <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
            {!!userProfile && <UserAvatar user={userProfile} />}
            <div className="grid flex-1 text-left text-sm leading-tight">
              <span className="truncate font-medium">{fullName}</span>
              <span className="text-muted-foreground truncate text-xs">
                {userProfile.email}
              </span>
            </div>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            <IconUserCircle />
            Account
          </DropdownMenuItem>
          <DropdownMenuItem>
            <IconCreditCard />
            Billing
          </DropdownMenuItem>
          <DropdownMenuItem>
            <IconNotification />
            Notifications
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />

        <DropdownMenuItem asChild>
          <ProgressLink href="/logout">
            <IconLogout />
            Log out
          </ProgressLink>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
