import {
  UserGoals,
  UserProfile,
  UserProfileUpdate,
  UserSettings,
  UserSettingsUpdate,
  UserWithSettings
} from '@/models/user/UserProfile';

import { BaseEndpoint } from '../../BaseEndpoint';
import { PracticeApi } from '../PracticeApi';

/**
 * Users endpoint group for the Practice API
 * Provides methods for user-related operations
 */
export class UsersEndpoint extends BaseEndpoint {
  private _currentUserUrl: string = 'me';

  constructor(api: PracticeApi) {
    super(api, { urlPrefix: 'users' });
  }

  /**
   * Get current user profile
   * @return {Promise<UserProfile>}
   */
  public async getProfile(): Promise<UserProfile> {
    const res = await this.get(this._currentUserUrl);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Update current user profile
   * @param {UserProfileUpdate} profileData - The profile data to update
   * @return {Promise<UserProfile>}
   */
  public async updateProfile(
    profileData: UserProfileUpdate
  ): Promise<UserProfile> {
    const res = await this.put(this._currentUserUrl, profileData);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get current user settings
   * @return {Promise<UserSettings>}
   */
  public async getSettings(): Promise<UserSettings> {
    const res = await this.get(`${this._currentUserUrl}/settings`);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Update current user settings
   * @param {UserSettingsUpdate} settingsData - The settings data to update
   * @return {Promise<UserSettings>}
   */
  public async updateSettings(
    settingsData: UserSettingsUpdate
  ): Promise<UserSettings> {
    const res = await this.put(
      `${this._currentUserUrl}/settings`,
      settingsData
    );
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get current user profile and settings combined
   * @return {Promise<UserWithSettings>}
   */
  public async getAll(): Promise<UserWithSettings> {
    const res = await this.get(`${this._currentUserUrl}/all`);
    await this._api.checkForError(res);
    return await res.json();
  }

  /**
   * Get current user's practice goals
   * @return {Promise<UserGoals>}
   */
  public async getGoals(): Promise<UserGoals> {
    const res = await this.get(`${this._currentUserUrl}/goals`);
    await this._api.checkForError(res);
    return await res.json();
  }
}
