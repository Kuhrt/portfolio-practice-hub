import { IApiOptions } from '@/models/api/ApiOptions';
import ConfigService from '@/services/ConfigService';
import { getErrorMessage } from '@/utils/errors';

import { ApiService } from '../ApiService';
import { PracticeGoalsEndpoint } from './endpoints/PracticeGoalsEndpoint';
import { PracticeSessionsEndpoint } from './endpoints/PracticeSessionsEndpoint';
import { UsersEndpoint } from './endpoints/UsersEndpoint';

export class PracticeApi extends ApiService {
  // Endpoint groups
  public readonly users: UsersEndpoint;
  public readonly goals: PracticeGoalsEndpoint;
  public readonly sessions: PracticeSessionsEndpoint;

  /**
   * Creates an API service with proper settings
   * @param {IApiOptions} options - The options for the API service
   */
  constructor(options: IApiOptions) {
    super(options);

    // Initialize endpoint groups
    this.users = new UsersEndpoint(this);
    this.goals = new PracticeGoalsEndpoint(this);
    this.sessions = new PracticeSessionsEndpoint(this);
  }

  /**
   * Tests the incoming response for an error object and returns the appropriate error message
   * @param {Response} response - The response to check for errors
   * @throws {Error} - With a string message
   */
  public async checkForError(response: Response) {
    if (!response.ok) {
      const contentType = response.headers.get('Content-Type');
      const resError = contentType?.includes('application/json')
        ? await response.json()
        : contentType?.includes('text/plain')
          ? await response.text()
          : `${response.status} - ${response.statusText}`;

      throw new Error(getErrorMessage(resError));
    }
  }

  protected async getBaseUrl(): Promise<string> {
    const config = await ConfigService.getClientConfig();
    return config.apiBaseUrl ?? '/api/';
  }
}
