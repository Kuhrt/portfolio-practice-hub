import {
  PracticeGoal,
  PracticeGoalCreate,
  PracticeGoalUpdate
} from '@/models/practice/PracticeGoal';

import { BaseEndpoint } from '../../BaseEndpoint';
import { PracticeApi } from '../PracticeApi';

/**
 * Practice Goals endpoint group for the Practice API
 * Provides methods for practice goal operations
 */
export class PracticeGoalsEndpoint extends BaseEndpoint {
  constructor(api: PracticeApi) {
    super(api, { urlPrefix: 'goals/practice' });
  }

  /**
   * Create a new practice goal
   * @param {PracticeGoalCreate} goalData - The goal data to create
   * @return {Promise<PracticeGoal>}
   */
  public async create(goalData: PracticeGoalCreate): Promise<PracticeGoal> {
    const res = await this.post('', goalData);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get all practice goals
   * @return {Promise<PracticeGoal[]>}
   */
  public async getAll(): Promise<PracticeGoal[]> {
    const res = await this.get('');
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get a practice goal by ID
   * @param {string} goalId - The goal ID
   * @return {Promise<PracticeGoal>}
   */
  public async getById(goalId: string): Promise<PracticeGoal> {
    const res = await this.get(goalId);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Update a practice goal
   * @param {string} goalId - The goal ID
   * @param {PracticeGoalUpdate} goalData - The updated goal data
   * @return {Promise<PracticeGoal>}
   */
  public async update(
    goalId: string,
    goalData: PracticeGoalUpdate
  ): Promise<PracticeGoal> {
    const res = await this.put(goalId, goalData);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Delete a practice goal
   * @param {string} goalId - The goal ID
   * @return {Promise<void>}
   */
  public async delete(goalId: string): Promise<void> {
    const res = await this.deleteRequest(goalId);
    await this._api.checkForError(res);
  }
}
