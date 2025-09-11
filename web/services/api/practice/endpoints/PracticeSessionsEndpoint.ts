import {
  PracticeSession,
  PracticeSessionCreate,
  PracticeSessionUpdate
} from '@/models/practice/PracticeSession';

import { BaseEndpoint } from '../../BaseEndpoint';
import { PracticeApi } from '../PracticeApi';

/**
 * Practice Sessions endpoint group for the Practice API
 * Provides methods for practice session operations
 */
export class PracticeSessionsEndpoint extends BaseEndpoint {
  constructor(api: PracticeApi) {
    super(api, { urlPrefix: 'sessions' });
  }

  /**
   * Create a new practice session
   * @param {PracticeSessionCreate} sessionData - The session data to create
   * @return {Promise<PracticeSession>}
   */
  public async create(
    sessionData: PracticeSessionCreate
  ): Promise<PracticeSession> {
    const res = await this.post('', sessionData);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get all practice sessions
   * @return {Promise<PracticeSession[]>}
   */
  public async getAll(): Promise<PracticeSession[]> {
    const res = await this.get('');
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get a practice session by ID
   * @param {string} sessionId - The session ID
   * @return {Promise<PracticeSession>}
   */
  public async getById(sessionId: string): Promise<PracticeSession> {
    const res = await this.get(sessionId);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Update a practice session
   * @param {string} sessionId - The session ID
   * @param {PracticeSessionUpdate} sessionData - The updated session data
   * @return {Promise<PracticeSession>}
   */
  public async update(
    sessionId: string,
    sessionData: PracticeSessionUpdate
  ): Promise<PracticeSession> {
    const res = await this.put(sessionId, sessionData);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Delete a practice session
   * @param {string} sessionId - The session ID
   * @return {Promise<void>}
   */
  public async delete(sessionId: string): Promise<void> {
    const res = await this.deleteRequest(sessionId);
    await this._api.checkForError(res);
  }
}
