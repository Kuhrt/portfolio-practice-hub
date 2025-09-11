import { auth, verifyJwtToken } from '.';

/**
 * Gets the auth token on the server side
 * NOTE: This is based on a generic JWT token auth flow. Update this method to match the backend provided.
 * @returns {(string | undefined)}
 */
export const getAuthToken = async () => {
  const session = await auth();
  const hasValidToken = verifyJwtToken(session?.accessToken);
  return hasValidToken ? session?.accessToken : undefined;
};
