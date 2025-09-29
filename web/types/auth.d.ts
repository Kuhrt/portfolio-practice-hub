// eslint-disable-next-line unused-imports/no-unused-imports
import { JWT } from 'next-auth/jwt';

import { TokenErrorEnum } from '@/models/auth/TokenErrorEnum';

declare module 'next-auth' {
  /**
   * The shape of the user object returned in the OAuth providers' `profile` callback,
   * or the second parameter of the `session` callback, when using a database.
   */
  interface User {
    roles?: string[];
    username?: string;
  }
  /**
   * The shape of the account object returned in the OAuth providers' `account` callback,
   * Usually contains information about the provider being used, like OAuth tokens (`access_token`, etc).
   */
  // interface Account {}

  /**
   * Returned by `useSession`, `auth`, contains information about the active session.
   */
  interface Session {
    accessToken?: string;
    tokenError?: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string;
    accessExpiresAt?: number;
    error?: TokenErrorEnum;
    refreshToken?: string;
    roles?: string[];
    username?: string;
  }
}
