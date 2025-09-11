/* eslint-disable @typescript-eslint/no-explicit-any */
import { IApiServiceOptions } from '@/models/api/ApiOptions';
import { ApiRequestOptions } from '@/models/api/ApiRequestOptions';
import { CleanUrlOptions } from '@/models/common/CleanUrlOptions';
import { KeyValue } from '@/models/common/KeyValue';

/**
 * Base API service that provides core functionality for making HTTP requests
 * This class can be extended to create specialized API services with custom
 * base URLs and error handling
 */
export abstract class ApiService {
  private _token?: string;

  protected _defaultRequestOptions: ApiRequestOptions;
  protected _headers: [string, string][] = [];
  protected _urlPrefix: string;

  /**
   * Creates a base API service with proper settings
   * @param {IApiOptions} options - Configuration options for the API service
   */
  constructor(options: IApiServiceOptions) {
    this._urlPrefix = options.urlPrefix ?? '';
    this._token = options.token;
    this._defaultRequestOptions = {
      isPublic: false,
      contentTypeMode: 'json'
    };
  }

  /**
   * Each subclass has it's own way of checking for errors
   * @param {Response} response
   */
  abstract checkForError(response: Response): Promise<void>;

  /**
   * Each subclass has it's own way of getting the base URL
   * @returns {Promise<string>}
   */
  protected abstract getBaseUrl(): Promise<string>;

  // * GETTERS
  protected get headers(): [string, string][] {
    return this._headers;
  }

  // * SETTERS
  protected set headers(newHeaders: KeyValue<string, string>[]) {
    for (const i in newHeaders) {
      const hasKeyProperty = Object.prototype.hasOwnProperty.call(
        newHeaders[i],
        'key'
      );
      const hasValueProperty = Object.prototype.hasOwnProperty.call(
        newHeaders[i],
        'value'
      );

      if (hasKeyProperty && hasValueProperty) {
        const key = newHeaders[i].key;
        const value = newHeaders[i].value;
        const existingHeader = this._headers.find(
          (header) => header[0] === key
        );
        if (!existingHeader) {
          this._headers.push([key, value]);
        } else {
          existingHeader[1] = value;
        }
      }
    }
  }

  // * METHODS
  /**
   * Adds or updates a header for requests
   * @param {string} key - The header key
   * @param {string} value - The header value
   */
  private setHeader(key: string, value: string) {
    const headerIndex = this._headers.findIndex((h) => h[0] == key);

    if (headerIndex < 0) {
      this._headers.push([key, value]);
    } else {
      this.headers[headerIndex][1] = value;
    }
  }

  /**
   * Ensures base url sections end with a slash so baseUrl will always end with a slash
   * @param {string} urlSection - The URL section to clean
   * @param {CleanUrlOptions} [options={checkFront: false}] - If true, will check and remove the front of the string for a slash
   * @returns {string} - The cleaned URL section
   */
  private cleanBaseUrlSection(
    urlSection: string,
    options?: CleanUrlOptions
  ): string {
    if (!urlSection) return '';

    const defaultOptions: CleanUrlOptions = {
      checkFront: false
    };
    const { checkFront } = { ...defaultOptions, ...options };
    if (urlSection === '') return '';
    if (checkFront && urlSection.startsWith('/')) {
      urlSection = urlSection.substring(1);
    }
    return urlSection.endsWith('/') ? urlSection : urlSection + '/';
  }

  /**
   * Gets the fully qualified URL to hit the API
   * @param {string} url - Path of the API endpoint
   * @returns {string} - The full URL
   */
  protected async buildFullUrl(url: string): Promise<string> {
    // Use custom base URL if provided, otherwise get from config
    let baseUrl = await this.getBaseUrl();

    baseUrl =
      this.cleanBaseUrlSection(baseUrl) +
      this.cleanBaseUrlSection(this._urlPrefix, {
        checkFront: true
      });

    const cleanedUrlPost = url.startsWith('/') ? url.substring(1) : url;
    let fullUrl = baseUrl + cleanedUrlPost;

    if (fullUrl.endsWith('/')) {
      fullUrl = fullUrl.substring(0, fullUrl.length - 1);
    }

    return fullUrl;
  }

  /**
   * Removes all headers from requests
   */
  private resetHeaders(): void {
    this._headers = [];
  }

  /**
   * Initializes all necessary settings for a request
   * @param {string} url
   * @param {ApiRequestOptions} [reqOptions] - The request options
   * @param {any} [body] - The request body
   * @returns {(any | undefined)} - The prepared request body
   */
  private async prepareRequest(
    url: string,
    reqOptions?: ApiRequestOptions,
    body?: any
  ) {
    const options = { ...this._defaultRequestOptions, ...reqOptions };

    // In case the same API object is used for multiple calls
    this.resetHeaders();

    // Authentication
    if (!options.isPublic && this._token) {
      this.setHeader('Authorization', `Bearer ${this._token}`);
    }

    // Content Type
    switch (options.contentTypeMode) {
      case 'json':
        this.setHeader('Content-Type', 'application/json');
        break;
      case 'form':
        // TODO: I had to remove it because it was causing an error for some reason
        break;
      default:
        this.setHeader('Content-Type', options.contentType ?? '');
        break;
    }

    // Body parsing
    let requestBody: any;
    if (!!body) {
      requestBody =
        options.contentTypeMode === 'json' ? JSON.stringify(body) : body;
    }

    const requestUrl = await this.buildFullUrl(url);

    return { requestBody, requestUrl };
  }

  // * DEFAULT API CALLS
  /**
   * Default GET request
   * @param {string} url - No leading slash
   * @param {ApiRequestOptions} [options] - Defaults to JSON content type
   * @returns {Promise<Response>} - The fetch response
   */
  async get(url: string, options?: ApiRequestOptions): Promise<Response> {
    const { requestUrl } = await this.prepareRequest(url, options);

    return await fetch(requestUrl, {
      method: 'GET',
      headers: this._headers,
      cache: options?.cache ?? 'default'
    });
  }

  /**
   * Default POST request
   * @param {string} url - No leading slash
   * @param {unknown} [body] - The request body
   * @param {ApiRequestOptions} [options] - Defaults to JSON content type
   * @returns {Promise<Response>} - The fetch response
   */
  async post(
    url: string,
    body?: any,
    options?: ApiRequestOptions
  ): Promise<Response> {
    const { requestBody, requestUrl } = await this.prepareRequest(
      url,
      options,
      body
    );

    return await fetch(requestUrl, {
      method: 'POST',
      headers: this._headers,
      body: requestBody,
      cache: options?.cache ?? 'default'
    });
  }

  /**
   * Default PUT request
   * @param {string} url - No leading slash
   * @param {any} body - The request body
   * @param {ApiRequestOptions} [options] - Defaults to JSON content type
   * @returns {Promise<Response>} - The fetch response
   */
  async put(
    url: string,
    body: any,
    options?: ApiRequestOptions
  ): Promise<Response> {
    const { requestBody, requestUrl } = await this.prepareRequest(
      url,
      options,
      body
    );
    return await fetch(requestUrl, {
      method: 'PUT',
      headers: this._headers,
      body: requestBody,
      cache: options?.cache ?? 'default'
    });
  }

  /**
   * Default PATCH request
   * @param {string} url - No leading slash
   * @param {any} body - The request body
   * @param {ApiRequestOptions} [options] - Defaults to JSON content type
   * @returns {Promise<Response>} - The fetch response
   */
  async patch(
    url: string,
    body: any,
    options?: ApiRequestOptions
  ): Promise<Response> {
    const { requestBody, requestUrl } = await this.prepareRequest(
      url,
      options,
      body
    );
    return await fetch(requestUrl, {
      method: 'PATCH',
      headers: this._headers,
      body: requestBody,
      cache: options?.cache ?? 'default'
    });
  }

  /**
   * Default DELETE request
   * @param {string} url - No leading slash
   * @param {ApiRequestOptions} [options] - Defaults to JSON content type
   * @param {any} [body] - The request body
   * @returns {Promise<Response>} - The fetch response
   */
  async delete(
    url: string,
    body?: any,
    options?: ApiRequestOptions
  ): Promise<Response> {
    const { requestBody, requestUrl } = await this.prepareRequest(
      url,
      options,
      body
    );
    return await fetch(requestUrl, {
      method: 'DELETE',
      headers: this._headers,
      body: requestBody,
      cache: options?.cache ?? 'default'
    });
  }
}
