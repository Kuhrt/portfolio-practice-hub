// Client-safe configuration values
export interface ClientConfig {
  apiBaseUrl: string;

  session: {
    checkInterval: number;
    refetchInterval: number;
  };
}
