'use client';

import { getSession } from 'next-auth/react';

import { verifyJwtToken } from '.';

/**
 * Gets the auth token on the client side
 * It will be very rare to use this as the token is included in the session which can use the useSession hook
 * NOTE: This is based on a generic JWT token auth flow. Update this method to match the backend provided.
 * @returns {(string | undefined)}
 */
export const getAuthToken = async () => {
  const session = await getSession();
  const hasValidToken = verifyJwtToken(session?.accessToken);
  return hasValidToken ? session?.accessToken : undefined;
};
