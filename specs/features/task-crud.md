# Task CRUD Operations

## User Stories

### User Story 1 - Create Tasks (Priority: P1)
As an authenticated user, I want to create new tasks so that I can organize my work and responsibilities.

**Why this priority**: Creating tasks is the fundamental functionality of a todo application.

**Independent Test**: User can successfully add a new task to their personal task list after authenticating.

**Acceptance Scenarios**:
1. Given I am logged in, When I submit a new task with a title, Then the task appears in my task list
2. Given I am logged in, When I submit a new task with title and description, Then the task appears in my task list with both fields preserved

---

### User Story 2 - View Task List (Priority: P1)
As an authenticated user, I want to view my list of tasks so that I can see what I need to do.

**Why this priority**: Viewing tasks is essential for the core functionality of a todo application.

**Independent Test**: User can see all their tasks in a list after authenticating.

**Acceptance Scenarios**:
1. Given I am logged in, When I navigate to the task list page, Then I see all my tasks
2. Given I am logged in with multiple tasks, When I refresh the page, Then I see all my tasks again

---

### User Story 3 - Update Tasks (Priority: P2)
As an authenticated user, I want to update my tasks so that I can modify their details as needed.

**Why this priority**: Allows users to modify existing tasks without recreating them.

**Independent Test**: User can modify the title or description of an existing task.

**Acceptance Scenarios**:
1. Given I am logged in and have a task, When I update the task title, Then the change is reflected in my task list
2. Given I am logged in and have a task, When I update the task description, Then the change is reflected in my task list

---

### User Story 4 - Delete Tasks (Priority: P2)
As an authenticated user, I want to delete tasks so that I can remove items I no longer need.

**Why this priority**: Allows users to clean up their task list by removing completed or irrelevant tasks.

**Independent Test**: User can remove a task from their task list permanently.

**Acceptance Scenarios**:
1. Given I am logged in and have a task, When I delete the task, Then it no longer appears in my task list
2. Given I am logged in and have multiple tasks, When I delete one task, Then only that task is removed from my list

---

### User Story 5 - Mark Task Complete/Incomplete (Priority: P2)
As an authenticated user, I want to mark tasks as complete or incomplete so that I can track my progress.

**Why this priority**: Essential for tracking task completion status.

**Independent Test**: User can toggle the completion status of their tasks.

**Acceptance Scenarios**:
1. Given I am logged in and have an incomplete task, When I mark it complete, Then its status updates to complete
2. Given I am logged in and have a completed task, When I mark it incomplete, Then its status updates to incomplete

## Acceptance Criteria
- All CRUD operations must be authenticated via JWT
- Users can only access their own tasks
- Task completion status can be toggled
- Tasks must have at least a title field

## Task Ownership
- Each task is associated with a specific authenticated user
- Users can only view, edit, or delete their own tasks
- The backend enforces user_id ownership on all operations

## Completion Toggle Behavior
- Tasks have a boolean 'completed' field that can be toggled
- Changing completion status updates the task in the database
- UI reflects the current completion status immediately