# REST API Endpoints

## Authentication Endpoints

### POST /api/auth/signup
Register a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (201 Created)**:
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses**:
- 400: Invalid input (e.g., weak password, invalid email)
- 409: Email already exists

### POST /api/auth/login
Authenticate a user and return JWT token.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Error Responses**:
- 400: Invalid input
- 401: Invalid credentials

### POST /api/auth/logout
End the user's session.

**Headers**:
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses**:
- 401: Invalid or expired token

## Task Management Endpoints

All task endpoints require JWT authentication in the Authorization header:

```
Authorization: Bearer {jwt_token}
```

### GET /api/tasks
Retrieve all tasks for the authenticated user.

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "task-uuid",
      "title": "Task title",
      "description": "Task description (optional)",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "user_id": "user-uuid"
    }
  ]
}
```

**Error Responses**:
- 401: Invalid or expired token

### POST /api/tasks
Create a new task for the authenticated user.

**Request**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Response (201 Created)**:
```json
{
  "id": "task-uuid",
  "title": "New task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

**Error Responses**:
- 400: Invalid input (e.g., missing title)
- 401: Invalid or expired token

### GET /api/tasks/{task_id}
Retrieve a specific task for the authenticated user.

**Response (200 OK)**:
```json
{
  "id": "task-uuid",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

**Error Responses**:
- 401: Invalid or expired token
- 403: Task belongs to another user
- 404: Task not found

### PUT /api/tasks/{task_id}
Update a specific task for the authenticated user.

**Request**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": "task-uuid",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

**Error Responses**:
- 400: Invalid input
- 401: Invalid or expired token
- 403: Task belongs to another user
- 404: Task not found

### PATCH /api/tasks/{task_id}/toggle
Toggle the completion status of a specific task.

**Response (200 OK)**:
```json
{
  "id": "task-uuid",
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

**Error Responses**:
- 401: Invalid or expired token
- 403: Task belongs to another user
- 404: Task not found

### DELETE /api/tasks/{task_id}
Delete a specific task for the authenticated user.

**Response (204 No Content)**:

**Error Responses**:
- 401: Invalid or expired token
- 403: Task belongs to another user
- 404: Task not found

## Error Cases

### 401 Unauthorized
Returned when:
- No Authorization header is provided
- JWT token is invalid or expired
- JWT token is malformed

### 403 Forbidden
Returned when:
- User attempts to access a task that belongs to another user
- User attempts to modify/delete a task that belongs to another user

### 404 Not Found
Returned when:
- Requested task does not exist
- Requested task belongs to the authenticated user but doesn't exist