import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { UserProfile } from '@/models/user';
import { cn } from '@/utils/styles';

interface Props {
  className?: string;
  user: UserProfile;
}

export function UserAvatar({ user, className }: Props) {
  const getUserInitials = () => {
    if (!user || (!user.first_name && !user.username)) return '';
    const fullName = user.first_name + ' ' + user.last_name;
    if (!fullName) return user?.username?.[0].toUpperCase() || '';

    const initials = fullName
      .trim()
      .split(' ')
      .map((n) => n[0])
      .join('');
    return initials.toUpperCase();
  };

  return (
    <Avatar className={cn('h-8 w-8 rounded-lg', className)}>
      {/* <AvatarImage src={user.image ?? ''} alt={user.name ?? user.username} /> */}
      <AvatarFallback className="rounded-lg">
        {getUserInitials()}
      </AvatarFallback>
    </Avatar>
  );
}
