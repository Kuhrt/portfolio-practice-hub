export interface IApiServiceOptions extends IApiOptions {
  /**
   * The path after the base URL that matches the group of endpoints (no slashes)
   */
  urlPrefix?: string;
}

export interface IApiOptions {
  /**
   * The token to use for the API requests
   */
  token?: string;
}
