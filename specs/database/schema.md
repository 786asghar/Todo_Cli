# Database Schema

## Overview
The database schema uses SQLModel ORM for defining tables and relationships. Neon Serverless PostgreSQL is used as the database backend.

## Users Table
Managed by Better Auth, the users table contains authentication information:

```sql
-- Managed by Better Auth
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Tasks Table
The tasks table stores todo items with ownership enforcement:

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Required Fields Only

### Tasks Table Fields:
- `id`: Unique identifier for each task (UUID, primary key)
- `title`: The task title (VARCHAR, not null)
- `completed`: Completion status (BOOLEAN, default false)
- `user_id`: Foreign key linking to the user who owns the task (UUID, not null)
- `created_at`: Timestamp when the task was created (TIMESTAMP)
- `updated_at`: Timestamp when the task was last updated (TIMESTAMP)

### Users Table Fields (Managed by Better Auth):
- `id`: Unique identifier for each user (UUID, primary key)
- `email`: User's email address (VARCHAR, unique, not null)
- `created_at`: Timestamp when the user was created (TIMESTAMP)
- `updated_at`: Timestamp when the user record was last updated (TIMESTAMP)

## SQLModel-Compatible Schema Definition

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: uuid.UUID

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Ownership Enforcement
- The `user_id` field in the tasks table enforces ownership
- Foreign key constraint ensures referential integrity
- Backend must verify that `user_id` matches the authenticated user's ID for all operations
- Cascade delete ensures tasks are removed when a user is deleted