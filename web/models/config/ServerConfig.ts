import { ClientConfig } from './ClientConfig';

// Server-only configuration values
export interface ServerConfig extends ClientConfig {
  auth: {
    secret: string;
    trustHost: boolean;
    keycloak: {
      url: string;
      id: string;
      realm: string;
      secret: string;
    };
  };
}
