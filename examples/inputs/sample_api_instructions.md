# Sample Project: REST API Development

## Goal
Develop a RESTful API for a task management application.

## Endpoints Required

### Tasks
- GET /api/tasks - List all tasks
- GET /api/tasks/{id} - Get specific task
- POST /api/tasks - Create new task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task

### Users
- POST /api/users/register - Register new user
- POST /api/users/login - User login
- GET /api/users/profile - Get user profile

## Data Models

### Task
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "pending|in_progress|completed",
  "priority": "low|medium|high",
  "due_date": "ISO8601 datetime",
  "created_at": "ISO8601 datetime",
  "user_id": "string"
}
```

### User
```json
{
  "id": "string",
  "username": "string",
  "email": "string",
  "created_at": "ISO8601 datetime"
}
```

## Requirements
1. Authentication required for all task endpoints
2. Users can only access their own tasks
3. Input validation on all endpoints
4. Proper HTTP status codes
5. JSON responses
6. Rate limiting: 100 requests per minute
7. CORS enabled
8. API versioning

## Questions
- Should we support pagination for task lists?
- What's the maximum number of tasks per user?
- Do we need task filtering and sorting?
- Should completed tasks be archived?

## Nice to Have
- Webhooks for task updates
- Task sharing between users
- Task comments
- File attachments
