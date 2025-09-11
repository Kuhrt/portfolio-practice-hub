export interface PracticeErrorResponse {
  /**
   * @todo Error should be an enum
   */
  error: string;
  message: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  details?: Record<string, any>;
  timestamp?: string;
  path?: string;
}
