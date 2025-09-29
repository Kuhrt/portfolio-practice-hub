import { QueryClient } from '@tanstack/react-query';

let browserQueryClient: QueryClient | undefined = undefined;
const makeQueryClient = () => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        refetchOnReconnect: false,
        staleTime: 60 * 1000
      }
    }
  });
};
export const getQueryClient = (isServer: boolean) => {
  if (isServer) {
    return makeQueryClient();
  } else {
    if (!browserQueryClient) browserQueryClient = makeQueryClient();
    return browserQueryClient;
  }
};
