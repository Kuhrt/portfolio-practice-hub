# Practice API Service

This service provides a clean, organized way to interact with the Practice API endpoints. It uses a pattern where endpoint groups are properties of the main API class, with each endpoint handling its own URL prefix.

## Usage

### Basic Setup

```typescript
import { PracticeApi } from '@/services/api/practice/PracticeApi';

// Create an API instance with authentication
// Note: No urlPrefix needed - each endpoint handles its own prefix
const api = new PracticeApi({
  token: 'your-auth-token'
});
```

### URL Structure

The API automatically handles URL construction with proper prefixes:

- **Base URL**: `{config.apiBaseUrl}` (e.g., "https://api.example.com" or "/api")
- **Users endpoints**: `{baseUrl}/users/me`, `/users/me/settings`, etc.
- **Goals endpoints**: `{baseUrl}/goals/practice`, `/goals/practice/{id}`, etc.
- **Sessions endpoints**: `{baseUrl}/sessions`, `/sessions/{id}`, etc.

If you had an API with a version prefix, it would be:

- **Base URL**: `{config.apiBaseUrl}/v1`
- **Users endpoints**: `{baseUrl}/v1/users/me`, etc.
- **Goals endpoints**: `{baseUrl}/v1/goals/practice`, etc.
- **Sessions endpoints**: `{baseUrl}/v1/sessions`, etc.

### Using Endpoint Groups

The API is organized into logical endpoint groups that you can access as properties:

#### Users Endpoints (`api.users`)

```typescript
// Get current user profile
const userProfile = await api.users.getProfile();
// Response: { id, email, username, first_name, last_name, display_name, timezone, last_login, created_at }

// Update user profile
const updatedProfile = await api.users.updateProfile({
  display_name: 'New Display Name',
  timezone: 'America/New_York'
});

// Get current user settings
const userSettings = await api.users.getSettings();
// Response: { default_session_type, preferred_tempo_range_min, daily_practice_goal_minutes, theme, etc. }

// Update user settings
const updatedSettings = await api.users.updateSettings({
  theme: 'dark',
  daily_practice_goal_minutes: 45,
  profile_public: true
});

// Get user profile and settings combined
const userAll = await api.users.getAll();
// Response: { profile: UserProfile, settings: UserSettings }

// Get user's practice goals
const userGoals = await api.users.getGoals();
// Response: { practice_goals: PracticeGoal[] }
```

#### Practice Goals Endpoints (`api.goals`)

```typescript
// Create a new practice goal
const newGoal = await api.goals.create({
  title: 'Learn Jazz Improvisation',
  description: 'Practice jazz scales and chord progressions',
  target: 30,
  target_type: PracticeTargetType.MINUTES,
  target_interval: PracticeInterval.DAILY,
  instrument: 'Piano'
});

// Get all practice goals
const allGoals = await api.goals.getAll();

// Get a specific goal
const goal = await api.goals.getById(goalId);

// Update a goal
const updatedGoal = await api.goals.update(goalId, {
  title: 'Updated Goal Title',
  status: GoalStatus.IN_PROGRESS
});

// Delete a goal
await api.goals.delete(goalId);
```

#### Practice Sessions Endpoints (`api.sessions`)

```typescript
// Create a new practice session
const newSession = await api.sessions.create({
  session_type: SessionType.PRACTICE,
  tempo: 120,
  difficulty_level: 3,
  instrument: 'Piano',
  notes: 'Worked on scales and arpeggios'
});

// Get all practice sessions
const allSessions = await api.sessions.getAll();

// Get a specific session
const session = await api.sessions.getById(sessionId);

// Update a session
const updatedSession = await api.sessions.update(sessionId, {
  rating: 4,
  notes: 'Great progress today!'
});

// Delete a session
await api.sessions.delete(sessionId);
```

## Complete API Reference

### Users Endpoints (`api.users`)

| Method                 | Description               | Request              | Response           |
| ---------------------- | ------------------------- | -------------------- | ------------------ |
| `getProfile()`         | Get current user profile  | -                    | `UserProfile`      |
| `updateProfile(data)`  | Update user profile       | `UserProfileUpdate`  | `UserProfile`      |
| `getSettings()`        | Get user settings         | -                    | `UserSettings`     |
| `updateSettings(data)` | Update user settings      | `UserSettingsUpdate` | `UserSettings`     |
| `getAll()`             | Get profile + settings    | -                    | `UserWithSettings` |
| `getGoals()`           | Get user's practice goals | -                    | `UserGoals`        |

### Practice Goals Endpoints (`api.goals`)

| Method             | Description     | Request              | Response         |
| ------------------ | --------------- | -------------------- | ---------------- |
| `create(data)`     | Create new goal | `PracticeGoalCreate` | `PracticeGoal`   |
| `getAll()`         | Get all goals   | -                    | `PracticeGoal[]` |
| `getById(id)`      | Get goal by ID  | -                    | `PracticeGoal`   |
| `update(id, data)` | Update goal     | `PracticeGoalUpdate` | `PracticeGoal`   |
| `delete(id)`       | Delete goal     | -                    | `void`           |

### Practice Sessions Endpoints (`api.sessions`)

| Method             | Description        | Request                 | Response            |
| ------------------ | ------------------ | ----------------------- | ------------------- |
| `create(data)`     | Create new session | `PracticeSessionCreate` | `PracticeSession`   |
| `getAll()`         | Get all sessions   | -                       | `PracticeSession[]` |
| `getById(id)`      | Get session by ID  | -                       | `PracticeSession`   |
| `update(id, data)` | Update session     | `PracticeSessionUpdate` | `PracticeSession`   |
| `delete(id)`       | Delete session     | -                       | `void`              |

## Architecture

### Base Classes

- **`ApiService`**: The base class that provides core HTTP functionality (GET, POST, PUT, DELETE, etc.)
- **`PracticeApi`**: Extends `ApiService` with Practice API-specific configuration and error handling
- **`BaseEndpoint`**: Base class for all endpoint groups that handles URL prefix management

### Endpoint Groups

- **`UsersEndpoint`**: Handles user-related operations (profile, settings, goals)
- **`PracticeGoalsEndpoint`**: Manages practice goals (CRUD operations)
- **`PracticeSessionsEndpoint`**: Manages practice sessions (CRUD operations)

### URL Prefix Management

Each endpoint group defines its own URL prefix:

```typescript
// UsersEndpoint
constructor(api: PracticeApi) {
  super(api, { urlPrefix: 'users' });
}

// PracticeGoalsEndpoint
constructor(api: PracticeApi) {
  super(api, { urlPrefix: 'goals/practice' });
}

// PracticeSessionsEndpoint
constructor(api: PracticeApi) {
  super(api, { urlPrefix: 'sessions' });
}
```

The `BaseEndpoint` class provides a `buildUrl()` helper method that combines the endpoint's prefix with the provided path:

```typescript
// In UsersEndpoint
const res = await this._api.get(this.buildUrl('me/settings'));
// Results in: {baseUrl}/users/me/settings
```

### Benefits of This Pattern

1. **Discoverability**: All available endpoints are easily discoverable through IntelliSense
2. **Organization**: Related endpoints are grouped logically
3. **Maintainability**: Easy to add new endpoint groups or modify existing ones
4. **Type Safety**: Full TypeScript support with proper typing for requests and responses
5. **Consistency**: All endpoints follow the same patterns and conventions
6. **Flexible URL Structure**: Each endpoint manages its own prefix, allowing for complex API structures

## Adding New Endpoint Groups

To add a new endpoint group:

1. Create a new endpoint class extending `BaseEndpoint`
2. Define the endpoint's URL prefix in the constructor
3. Add the endpoint as a property in `PracticeApi`
4. Initialize it in the constructor

Example:

```typescript
// endpoints/NewEndpoint.ts
export class NewEndpoint extends BaseEndpoint {
  constructor(api: PracticeApi) {
    super(api, { urlPrefix: 'new-endpoint' });
  }

  public async someMethod(): Promise<SomeType> {
    const res = await this._api.get(this.buildUrl('some-path'));
    await this._api.checkForError(res);
    return await res.json();
  }
}

// PracticeApi.ts
export class PracticeApi extends ApiService {
  public readonly newEndpoint: NewEndpoint;

  constructor(options: IApiOptions) {
    super(options);
    this.newEndpoint = new NewEndpoint(this);
  }
}
```

## Error Handling

All endpoints automatically handle errors through the `checkForError` method, which:

- Checks if the response is successful
- Parses error messages from different content types
- Throws meaningful error messages

## Authentication

The API automatically includes the Bearer token in the Authorization header for all requests when a token is provided during initialization.
