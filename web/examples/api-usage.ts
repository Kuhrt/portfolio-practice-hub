/**
 * Example usage of the new Practice API pattern
 * This demonstrates how to use the refactored API with endpoint groups
 * and proper URL prefix handling
 */

import { PracticeApi } from '@/services/api/practice/PracticeApi';
import {
  PracticeTargetType,
  PracticeInterval,
  SessionType
} from '@/models/practice';

// Example: Initialize the API with authentication
// Note: No urlPrefix needed here - each endpoint handles its own prefix
const api = new PracticeApi({
  token: 'your-auth-token-here'
});

// Example: User operations
// These will hit: {config.apiBaseUrl}/users/me, /users/me/settings, etc.
async function userExamples() {
  try {
    // Get current user profile
    const userProfile = await api.users.getProfile();
    console.log('User profile:', userProfile);

    // Get current user settings
    const userSettings = await api.users.getSettings();
    console.log('User settings:', userSettings);

    // Get user profile and settings combined
    const userAll = await api.users.getAll();
    console.log('User profile and settings:', userAll);

    // Get user's practice goals
    const userGoals = await api.users.getGoals();
    console.log('User practice goals:', userGoals);

    // Update user profile
    const updatedProfile = await api.users.updateProfile({
      display_name: 'Updated Display Name',
      timezone: 'America/New_York'
    });
    console.log('Updated profile:', updatedProfile);

    // Update user settings
    const updatedSettings = await api.users.updateSettings({
      theme: 'dark',
      daily_practice_goal_minutes: 45,
      profile_public: true
    });
    console.log('Updated settings:', updatedSettings);
  } catch (error) {
    console.error('Error with user operations:', error);
  }
}

// Example: Practice Goals operations
// These will hit: {config.apiBaseUrl}/goals/practice, /goals/practice/{id}, etc.
async function goalExamples() {
  try {
    // Create a new practice goal
    const newGoal = await api.goals.create({
      title: 'Master Jazz Piano',
      description: 'Learn jazz theory and improvisation techniques',
      target: 60, // 60 minutes
      target_type: PracticeTargetType.MINUTES,
      target_interval: PracticeInterval.DAILY,
      instrument: 'Piano',
      priority: 1
    });
    console.log('Created goal:', newGoal);

    // Get all goals
    const allGoals = await api.goals.getAll();
    console.log('All goals:', allGoals);

    // Update a goal
    if (allGoals.length > 0) {
      const updatedGoal = await api.goals.update(allGoals[0].id, {
        title: 'Master Jazz Piano - Advanced',
        priority: 2
      });
      console.log('Updated goal:', updatedGoal);
    }
  } catch (error) {
    console.error('Error with goals:', error);
  }
}

// Example: Practice Sessions operations
// These will hit: {config.apiBaseUrl}/sessions, /sessions/{id}, etc.
async function sessionExamples() {
  try {
    // Create a new practice session
    const newSession = await api.sessions.create({
      session_type: SessionType.PRACTICE,
      tempo: 120,
      difficulty_level: 3,
      instrument: 'Piano',
      notes: 'Worked on jazz scales and chord progressions'
    });
    console.log('Created session:', newSession);

    // Get all sessions
    const allSessions = await api.sessions.getAll();
    console.log('All sessions:', allSessions);

    // Update a session
    if (allSessions.length > 0) {
      const updatedSession = await api.sessions.update(allSessions[0].id, {
        rating: 4,
        notes: 'Great progress! Really getting the hang of the scales.'
      });
      console.log('Updated session:', updatedSession);
    }
  } catch (error) {
    console.error('Error with sessions:', error);
  }
}

// Example: Complete workflow
async function completeWorkflow() {
  console.log('=== Complete Practice API Workflow ===');

  await userExamples();
  await goalExamples();
  await sessionExamples();

  console.log('=== Workflow Complete ===');
}

// Example: URL Structure Explanation
function explainUrlStructure() {
  console.log(`
URL Structure:
- Base URL: {config.apiBaseUrl} (e.g., "https://api.example.com" or "/api")
- Users endpoints: {baseUrl}/users/me, /users/me/settings, etc.
- Goals endpoints: {baseUrl}/goals/practice, /goals/practice/{id}, etc.
- Sessions endpoints: {baseUrl}/sessions, /sessions/{id}, etc.

If you had an API with a version prefix, it would be:
- Base URL: {config.apiBaseUrl}/v1
- Users endpoints: {baseUrl}/v1/users/me, etc.
- Goals endpoints: {baseUrl}/v1/goals/practice, etc.
- Sessions endpoints: {baseUrl}/v1/sessions, etc.

The beauty of this system is that endpoint developers don't need to worry about URL construction:
- In UsersEndpoint: this.get('me') automatically becomes {baseUrl}/users/me
- In PracticeGoalsEndpoint: this.post('', data) automatically becomes {baseUrl}/goals/practice
- In PracticeSessionsEndpoint: this.get('123') automatically becomes {baseUrl}/sessions/123
  `);
}

// Export for use in other files
export {
  completeWorkflow,
  userExamples,
  goalExamples,
  sessionExamples,
  explainUrlStructure
};
