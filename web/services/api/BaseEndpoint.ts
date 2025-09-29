import { ApiRequestOptions } from '@/models/api/ApiRequestOptions';
import { IEndpointOptions } from '@/models/api/IEndpointOptions';

import { PracticeApi } from './practice/PracticeApi';

/**
 * Base endpoint class that provides common functionality for all endpoint groups
 * Handles URL prefix management automatically by wrapping API calls
 */
export abstract class BaseEndpoint {
  protected readonly _urlPrefix: string;

  constructor(
    protected _api: PracticeApi,
    options: IEndpointOptions
  ) {
    this._urlPrefix = options.urlPrefix;
  }

  /**
   * Builds a full URL by combining the endpoint's prefix with the provided path
   * @param {string} path - The path to append to the endpoint prefix
   * @returns {string} - The full URL path
   */
  private buildUrl(path: string = ''): string {
    if (!path) {
      return this._urlPrefix;
    }

    // Remove leading slash from path if present
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;

    // Combine prefix with path
    return `${this._urlPrefix}/${cleanPath}`;
  }

  /**
   * Wrapper for API GET requests that automatically applies the endpoint prefix
   */
  protected async get(path: string, options?: ApiRequestOptions) {
    return this._api.get(this.buildUrl(path), options);
  }

  /**
   * Wrapper for API POST requests that automatically applies the endpoint prefix
   */
  protected async post(
    path: string,
    body?: unknown,
    options?: ApiRequestOptions
  ) {
    return this._api.post(this.buildUrl(path), body, options);
  }

  /**
   * Wrapper for API PUT requests that automatically applies the endpoint prefix
   */
  protected async put(
    path: string,
    body?: unknown,
    options?: ApiRequestOptions
  ) {
    return this._api.put(this.buildUrl(path), body, options);
  }

  /**
   * Wrapper for API PATCH requests that automatically applies the endpoint prefix
   */
  protected async patch(
    path: string,
    body?: unknown,
    options?: ApiRequestOptions
  ) {
    return this._api.patch(this.buildUrl(path), body, options);
  }

  /**
   * Wrapper for API DELETE requests that automatically applies the endpoint prefix
   */
  protected async deleteRequest(
    path: string,
    body?: unknown,
    options?: ApiRequestOptions
  ) {
    return this._api.delete(this.buildUrl(path), body, options);
  }
}
