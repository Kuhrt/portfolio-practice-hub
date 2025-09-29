import jwt from 'jsonwebtoken';
import { DateTime } from 'luxon';
import NextAuth from 'next-auth';
import Keycloak from 'next-auth/providers/keycloak';

import { AUTH_TOKEN_NAME } from '@/constants/auth';
import { TokenErrorEnum } from '@/models/auth/TokenErrorEnum';
import { TokenRole, TokenRoles } from '@/models/auth/TokenRoles';
import ConfigService from '@/services/ConfigService';

/**
 * Ensures a JWT token is valid.
 * @param {string} [token]
 * @returns {boolean}
 */
export const verifyJwtToken = (token?: string) => {
  if (!token?.length) return false;

  const decodedToken = jwt.decode(token);
  if (!decodedToken || typeof decodedToken === 'string' || !decodedToken.exp)
    return false;

  const now = DateTime.utc().toSeconds();
  return now < decodedToken.exp;
};

/**
 * Returns the Keycloak roles from the token object.
 * @param token - Set to any to avoid type errors
 * @returns {string[]} roles
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const getRolesFromToken = (token: any) => {
  const roles: string[] = [];

  // * Keycloak puts roles under resource_access and realm_access properties
  if (!!token.realm_access) {
    const realmAccess = token.realm_access as TokenRole;
    roles.push(...(realmAccess.roles as string[]));
  }
  if (!!token.resource_access) {
    const resourceAccess = token.resource_access as TokenRoles;
    if (!!resourceAccess) {
      Object.keys(resourceAccess).forEach((key) => {
        roles.push(...resourceAccess[key].roles);
      });
    }
  }

  return roles;
};

export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    authorized: ({ auth }) => {
      // Logged in users are authenticated, otherwise redirect to login page
      return !!auth;
    },
    async jwt({ account, token, trigger }) {
      const appConfig = ConfigService.getServerConfig();
      const nowPlusRefreshTime = DateTime.now()
        .plus({ milliseconds: appConfig.session.refetchInterval })
        .toSeconds();

      // * Persist any custom data we want on the token manually
      // * If account exists, it is the first time the user logged in
      if (!!account) {
        if (!!account.access_token) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const tokenObj = jwt.decode(account.access_token) as any;

          let roles: string[] = [];
          if (!!tokenObj && typeof tokenObj !== 'string') {
            roles = getRolesFromToken(tokenObj);
          }

          token.accessToken = account.access_token;
          token.username = tokenObj.preferred_username;
          token.roles = roles;
        }

        token.accessExpiresAt = account.expires_at;
        token.refreshToken = account.refresh_token;
        token.error = undefined;

        // * If the access token needs to be refreshed
      } else if (
        !!token &&
        (trigger === 'update' ||
          (!!token.accessExpiresAt &&
            token.accessExpiresAt < nowPlusRefreshTime))
      ) {
        if (!token.refreshToken) throw new TypeError('Missing refresh token');

        try {
          const appConfig = ConfigService.getServerConfig();
          const response = await fetch(
            `${appConfig.auth.keycloak.url}/realms/${appConfig.auth.keycloak.realm}/protocol/openid-connect/token`,
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
              },
              body: new URLSearchParams({
                client_id: appConfig.auth.keycloak.id,
                client_secret: appConfig.auth.keycloak.secret,
                grant_type: 'refresh_token',
                refresh_token: token.refreshToken
              })
            }
          );

          const newTokens = await response.json();
          if (!response.ok || !newTokens)
            throw new Error(
              !!newTokens?.error_description
                ? newTokens.error_description
                : !!newTokens?.error && typeof newTokens.error === 'string'
                  ? newTokens.error
                  : 'Failed to refresh the access token'
            );

          token.accessToken = newTokens.access_token;
          token.accessExpiresAt = Math.floor(
            DateTime.now().toSeconds() + newTokens.expires_in
          );
          if (!!newTokens.refresh_token)
            token.refreshToken = newTokens.refresh_token;
          token.error = undefined;
          trigger = 'update';
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (_) {
          token.error = TokenErrorEnum.REFRESH_FAILED;
        }
      }

      return token;
    },
    session: ({ session, token }) => {
      // * Data can also be persisted to the session similarly to the token
      if (!!session?.user) {
        if (!session.user.roles && !!token?.roles) {
          session.user.roles = token.roles;
        }
        if (!session.user.username && !!token?.username) {
          session.user.username = token.username;
        }
        // TODO: This is not the actual id, it's the "subject" id. This changes every login. Need to research if we can get the actual id or if we can get the right users from their subject ids.
        if (!session.user.id && !!token?.sub) {
          session.user.id = token.sub;
        }
      }

      if (!!token?.accessToken) {
        session.accessToken = token.accessToken;
      }

      session.tokenError = token?.error;

      return session;
    }
  },
  cookies: {
    sessionToken: {
      name: AUTH_TOKEN_NAME
    }
  },
  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/login/error'
  },
  providers: [
    Keycloak({
      issuer: `${ConfigService.getServerConfig().auth.keycloak.url}/realms/${ConfigService.getServerConfig().auth.keycloak.realm}`,
      clientId: ConfigService.getServerConfig().auth.keycloak.id,
      clientSecret: ConfigService.getServerConfig().auth.keycloak.secret
    })
  ],
  session: {
    updateAge: 0
  }
});
