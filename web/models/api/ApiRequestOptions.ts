/**
 * This is used to specify options for an API request
 */
export interface ApiRequestOptions {
  /**
   * If true, the request will not include an auth token
   */
  isPublic?: boolean;
  contentTypeMode?: 'json' | 'form' | 'other';
  /**
   * This is used for the content-type header if contentTypeMode is set to 'other'
   */
  contentType?: string;
  cache?:
    | 'no-cache'
    | 'no-store'
    | 'default'
    | 'reload'
    | 'force-cache'
    | 'only-if-cached';
}
