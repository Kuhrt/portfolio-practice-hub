import { ClientConfig } from '@/models/config/ClientConfig';
import { ServerConfig } from '@/models/config/ServerConfig';
import { isBrowser } from '@/utils/browser';

/**
 * ConfigService is a singleton class that provides configuration values for the application
 * It can be used to get configuration values for the client-side and server-side
 * Replaces Next's config service in favor of always having run-time configuration values
 */
class ConfigService {
  private static instance: ConfigService;
  private clientConfigCache: ClientConfig | null = null;
  private serverConfigCache: ServerConfig | null = null;
  public nodeEnv: string = process.env.NODE_ENV || 'development';

  private constructor() {
    // Initialize anything for client-side only
    // if (isBrowser()) {}
  }

  public static getInstance(): ConfigService {
    if (!ConfigService.instance) {
      ConfigService.instance = new ConfigService();
    }
    return ConfigService.instance;
  }

  /**
   * Gets configuration values safe for client-side use
   */
  public async getClientConfig(): Promise<ClientConfig> {
    if (isBrowser()) {
      return this.getClientConfigFromApi();
    } else {
      return this.getClientConfigFromEnv();
    }
  }

  /**
   * Gets full configuration including server-only values
   * Only works on server-side
   */
  public getServerConfig(): ServerConfig {
    if (isBrowser()) {
      throw new Error(
        'Server configuration cannot be accessed from client-side'
      );
    }

    if (this.serverConfigCache) {
      return this.serverConfigCache;
    }

    const clientConfig = this.getClientConfigFromEnv();

    this.serverConfigCache = {
      ...clientConfig,
      auth: {
        secret: process.env.AUTH_SECRET || '',
        trustHost: process.env.AUTH_TRUST_HOST === 'true',
        keycloak: {
          url: process.env.AUTH_KEYCLOAK_URL || '',
          id: process.env.AUTH_KEYCLOAK_ID || '',
          realm: process.env.AUTH_KEYCLOAK_REALM || '',
          secret: process.env.AUTH_KEYCLOAK_SECRET || ''
        }
      }
    };

    return this.serverConfigCache;
  }

  /**
   * Gets a specific configuration value
   * Automatically determines client vs server context
   */
  public async get<T = string>(key: string): Promise<T | undefined> {
    if (isBrowser()) {
      const config = await this.getClientConfig();
      return this.getNestedValue(config, key) as T;
    } else {
      const config = this.getServerConfig();
      return this.getNestedValue(config, key) as T;
    }
  }

  /**
   * Checks if a configuration value exists
   */
  public async has(key: string): Promise<boolean> {
    const value = await this.get(key);
    return value !== undefined && value !== null && value !== '';
  }

  /**
   * Clears the configuration cache
   */
  public clearCache(): void {
    this.clientConfigCache = null;
    this.serverConfigCache = null;
  }

  private async getClientConfigFromApi(): Promise<ClientConfig> {
    if (this.clientConfigCache) {
      return this.clientConfigCache;
    }

    try {
      const response = await fetch('/api/config/client');
      if (!response.ok) {
        throw new Error(
          `Failed to fetch client config: ${response.statusText}`
        );
      }
      const clientConfig: ClientConfig = await response.json();
      this.clientConfigCache = clientConfig;
      return this.clientConfigCache;
    } catch (error) {
      console.error('Failed to fetch client configuration:', error);
      throw new Error('Unable to load application configuration');
    }
  }

  private getClientConfigFromEnv(): ClientConfig {
    if (this.clientConfigCache) {
      return this.clientConfigCache;
    }

    this.clientConfigCache = {
      apiBaseUrl: process.env.API_BASE_URL || '/api/',

      session: {
        checkInterval:
          !process.env.SESSION_CHECK_INTERVAL ||
          isNaN(+process.env.SESSION_CHECK_INTERVAL)
            ? 1000
            : +process.env.SESSION_CHECK_INTERVAL,
        refetchInterval:
          !process.env.SESSION_REFETCH_INTERVAL ||
          isNaN(+process.env.SESSION_REFETCH_INTERVAL)
            ? 60000
            : +process.env.SESSION_REFETCH_INTERVAL
      }
    };

    return this.clientConfigCache;
  }

  /**
   * Helper to get nested object values using dot notation
   * e.g., 'auth.keycloak.url' -> config.auth.keycloak.url
   */
  private getNestedValue(
    obj: ClientConfig | ServerConfig,
    path: string
  ): unknown {
    return path.split('.').reduce((current: unknown, key) => {
      if (current && typeof current === 'object' && key in current) {
        return (current as Record<string, unknown>)[key];
      }
      return undefined;
    }, obj);
  }
}

// Export singleton instance
export default ConfigService.getInstance();
