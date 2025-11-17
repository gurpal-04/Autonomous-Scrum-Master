# Sprint Planning API

The Sprint Planning API has been updated to work with the sprint planner agent that requires structured data. **Planning results are stored as task IDs in the sprint document for simplicity and efficiency.**

## Overview

The sprint planner agent expects specific data structures for tasks and developers to create an optimal sprint plan. The API now supports two modes:

1. **Explicit data mode**: Provide tasks and developers directly in the request
2. **Firestore mode**: Automatically fetch tasks and developers from the database

**Database Storage**: Planning results are stored efficiently in the sprint document:

- Sprint records with metadata and planned task IDs
- Individual task documents with assignments
- Activity logs for tracking planning events

## API Endpoints

### Planning

```
POST /sprint/plan
```

### Task Management

```
GET /sprint/{sprint_id}/tasks                    # Get all tasks in sprint
POST /sprint/{sprint_id}/tasks                   # Add task IDs to sprint
DELETE /sprint/{sprint_id}/tasks                 # Remove task IDs from sprint
POST /sprint/{sprint_id}/assignments             # Update task assignments
```

### Sprint Management

```
GET /sprint/{sprint_id}                          # Get sprint details
GET /sprint/                                      # List all sprints
```

## Getting Tasks for a Sprint

### **GET /sprint/{sprint_id}/tasks**

This endpoint retrieves all tasks that are planned for a specific sprint.

**Parameters:**

- `sprint_id` (path parameter): The ID of the sprint

**Response:**

```json
{
  "tasks": [
    {
      "id": "task1",
      "title": "Implement user authentication",
      "description": "Create login/logout functionality with JWT tokens",
      "role": "backend",
      "estimate_hours": 16,
      "sprint_points": 8,
      "assigned_to": "Alice Johnson",
      "status": "scheduled",
      "sprint_id": "abc123",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "task2",
      "title": "Design login page UI",
      "description": "Create responsive login form with validation",
      "role": "frontend",
      "estimate_hours": 12,
      "sprint_points": 5,
      "assigned_to": "Bob Smith",
      "status": "scheduled",
      "sprint_id": "abc123",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Example Usage:**

```python
import requests

# Get all tasks for a sprint
sprint_id = "abc123"
response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
tasks_data = response.json()

print(f"Number of tasks: {len(tasks_data['tasks'])}")
for task in tasks_data['tasks']:
    print(f"- {task['title']} (assigned to: {task.get('assigned_to', 'Unassigned')})")
```

```bash
curl -X GET "http://localhost:8080/sprint/abc123/tasks"
```

**Error Handling:**

- Returns empty tasks array for non-existent sprints
- Returns 500 for server errors

## Request Format

### Full Data Mode

```json
{
  "tasks": [
    {
      "title": "Implement user authentication",
      "description": "Create login/logout functionality with JWT tokens",
      "role": "backend",
      "estimate_hours": 16,
      "sprint_points": 8
    }
  ],
  "developers": [
    {
      "name": "Alice Johnson",
      "role": "backend",
      "available_hours_per_day": 6
    }
  ],
  "timeline_days": 10,
  "sprint_name": "Authentication Sprint",
  "sprint_goal": "Complete user authentication feature"
}
```

### Firestore Mode (Minimal Data)

```json
{
  "timeline_days": 14,
  "sprint_name": "Database Sprint",
  "sprint_goal": "Plan sprint using existing data"
}
```

When tasks or developers are not provided, the API will automatically fetch:

- Unassigned tasks from the Firestore `tasks` collection
- Available developers from the Firestore `developers` collection

## Data Models

### SprintTask

- `title` (string): Task title
- `description` (string): Detailed task description
- `role` (string): Required developer role (frontend, backend, fullstack, qa, etc.)
- `estimate_hours` (integer): Estimated completion time in hours
- `sprint_points` (integer): Story points using Fibonacci scale

### SprintDeveloper

- `name` (string): Developer name
- `role` (string): Developer's primary role
- `available_hours_per_day` (integer): Daily availability in hours

### SprintPlan

- `tasks` (optional): List of SprintTask objects
- `developers` (optional): List of SprintDeveloper objects
- `timeline_days` (optional): Number of days for the sprint
- `sprint_name` (optional): Name for the sprint
- `sprint_goal` (optional): Goal/objective for the sprint

## Response Format

### Planning Response

The API returns comprehensive planning results:

```json
{
  "sprint_id": "abc123",
  "planned_tasks": [
    {
      "title": "Implement user authentication",
      "description": "Create login/logout functionality with JWT tokens",
      "role": "backend",
      "estimate_hours": 16,
      "sprint_points": 8,
      "assigned_to": "Alice Johnson",
      "status": "scheduled",
      "planned_start_day": 1,
      "planned_end_day": 3
    }
  ],
  "planned_task_ids": ["task1", "task2", "task3"],
  "task_assignments": {
    "task1": "Alice Johnson",
    "task2": "Bob Smith"
  },
  "summary": {
    "total_tasks": 3,
    "scheduled_tasks": 2,
    "unassigned_tasks": 1,
    "team_size": 3,
    "timeline_days": 10
  }
}
```

### Planning Data Retrieval

```json
{
  "id": "plan456",
  "sprint_id": "abc123",
  "planned_tasks": [...],
  "planning_input": {
    "tasks": [...],
    "developers": [...],
    "timeline_days": 10
  },
  "planning_timestamp": "2024-01-15T10:30:00Z",
  "agent_response": "Raw agent response...",
  "status": "active"
}
```

## Database Storage Structure

### Sprint Collection

- **Document ID**: Auto-generated sprint ID
- **Fields**: name, goal, start_date, end_date, status, capacity, team_size, total_tasks, etc.

### Planning Subcollection

- **Path**: `sprints/{sprint_id}/planning/{plan_id}`
- **Fields**: planned_tasks, planning_input, planning_timestamp, agent_response, status

### Tasks Collection

- **Document ID**: Auto-generated task ID
- **Fields**: title, description, role, estimate_hours, sprint_points, assigned_to, status, sprint_id, task_type

### Activity Log Subcollection

- **Path**: `sprints/{sprint_id}/activity/{activity_id}`
- **Fields**: action, description, user, timestamp, plan_id, task_ids

## Example Usage

### Python Example

```python
import requests

# Full data mode
payload = {
    "tasks": [
        {
            "title": "Implement user authentication",
            "description": "Create login/logout functionality with JWT tokens",
            "role": "backend",
            "estimate_hours": 16,
            "sprint_points": 8
        }
    ],
    "developers": [
        {
            "name": "Alice Johnson",
            "role": "backend",
            "available_hours_per_day": 6
        }
    ],
    "timeline_days": 10,
    "sprint_name": "Authentication Sprint",
    "sprint_goal": "Complete user authentication feature"
}

# Create sprint plan
response = requests.post("http://localhost:8080/sprint/plan", json=payload)
result = response.json()
sprint_id = result["sprint_id"]

# Retrieve planning data
plan_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/plan")
plan_data = plan_response.json()

# Get all planning attempts
plans_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/plans")
all_plans = plans_response.json()

# Get sprint details
sprint_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}")
sprint_data = sprint_response.json()
```

### cURL Examples

```bash
# Create sprint plan
curl -X POST "http://localhost:8080/sprint/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {
        "title": "Implement user authentication",
        "description": "Create login/logout functionality with JWT tokens",
        "role": "backend",
        "estimate_hours": 16,
        "sprint_points": 8
      }
    ],
    "developers": [
      {
        "name": "Alice Johnson",
        "role": "backend",
        "available_hours_per_day": 6
      }
    ],
    "timeline_days": 10,
    "sprint_name": "Authentication Sprint",
    "sprint_goal": "Complete user authentication feature"
  }'

# Retrieve planning data
curl -X GET "http://localhost:8080/sprint/{sprint_id}/plan"

# List all planning attempts
curl -X GET "http://localhost:8080/sprint/{sprint_id}/plans"

# Get sprint details
curl -X GET "http://localhost:8080/sprint/{sprint_id}"
```

## Backward Compatibility

The API maintains backward compatibility with the old `SprintPlan` model fields:

- `sprint_goal`
- `available_stories`
- `team_capacity`
- `constraints`

These fields are now optional and can be used alongside the new task/developer structure.

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Successful planning or retrieval
- `400`: Invalid request data
- `404`: Sprint or plan not found
- `500`: Internal server error or agent execution error

## Testing

Run the comprehensive test file to verify all functionality:

```bash
python test/test_sprint_planning.py
```

This will test:

- Sprint planning with explicit data
- Sprint planning with Firestore data
- Database storage and retrieval
- Sprint details retrieval
- Planning history management
