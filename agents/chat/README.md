# Chat Agent with Function Tools

This directory contains the chat agent with integrated function tools for managing Scrum operations. The agent can handle various user queries related to tasks, epics, and developers.

## Overview

The chat agent is equipped with 15 function tools that allow it to perform CRUD operations on:

- **Tasks**: Create, read, update, delete, list, and assign developers
- **Epics**: Create, read, update, and list
- **Developers**: Create, read, update, delete, and list

## Available Tools

### Task Operations

1. **`create_task`** - Create a new task

   - Required: `title`, `description`, `priority`
   - Optional: `status`, `story_id`, `epic_id`, `estimated_hours`, `assignee_id`

2. **`list_tasks`** - List all tasks with optional filtering

   - Optional filters: `status`, `assignee_id`, `epic_id`, `priority`

3. **`get_task`** - Get details of a specific task

   - Required: `task_id`

4. **`update_task`** - Update task fields

   - Required: `task_id`
   - Optional updates: `title`, `description`, `priority`, `status`, `estimated_hours`, `assignee_id`

5. **`delete_task`** - Delete a task

   - Required: `task_id`

6. **`assign_developers_to_task`** - Assign developers to a task
   - Required: `task_id`, `developer_ids` (list)

### Epic Operations

7. **`create_epic`** - Create a new epic

   - Required: `title`, `description`, `priority`
   - Optional: `status`

8. **`list_epics`** - List all epics

9. **`get_epic`** - Get details of a specific epic

   - Required: `epic_id`

10. **`update_epic`** - Update epic fields
    - Required: `epic_id`
    - Optional updates: `title`, `description`, `priority`, `status`

### Developer Operations

11. **`create_developer`** - Create a new developer profile

    - Required: `name`, `email`, `skills` (list)
    - Optional: `availability`

12. **`list_developers`** - List all developers

13. **`get_developer`** - Get details of a specific developer

    - Required: `developer_id`

14. **`update_developer`** - Update developer profile

    - Required: `developer_id`
    - Optional updates: `name`, `email`, `skills`, `availability`

15. **`delete_developer`** - Delete a developer profile
    - Required: `developer_id`

## Common User Queries

The agent can handle natural language queries like:

- "Create a task called 'Fix login bug' with high priority"
- "List all tasks assigned to John"
- "Show tasks with status 'in_progress'"
- "Create an epic for user authentication"
- "Assign Jane to the database optimization task"
- "Update task ABC123 status to 'done'"
- "Create a developer profile for John Doe"
- "List all available developers"
- "Show tasks with high priority"

## Usage Examples

### Creating a Task

```
User: "Create a task called 'Fix login bug' with high priority"
Agent: Uses create_task tool with title="Fix login bug", priority="high"
```

### Listing Tasks with Filter

```
User: "Show me all tasks assigned to developer ABC123"
Agent: Uses list_tasks tool with assignee_id="ABC123"
```

### Assigning Developers

```
User: "Assign developers DEF456 and GHI789 to task XYZ123"
Agent: Uses assign_developers_to_task tool with task_id="XYZ123", developer_ids=["DEF456", "GHI789"]
```

## Configuration

### API Base URL

The tools are configured to connect to your API server. Update the `BASE_URL` in `tools.py` if your server runs on a different port or host:

```python
BASE_URL = "http://localhost:8080"  # Change this as needed
```

### Error Handling

All tools return structured responses with:

- `status`: "success" or "error"
- `message`: Success message or error details
- Additional fields specific to each operation

## Testing

Run the test script to verify all tools work correctly:

```bash
cd agents/chat
python test_tools.py
```

Make sure your API server is running before testing.

## Integration with ADK

The function tools are automatically wrapped by ADK when added to the agent's tools list. The agent can:

1. **Understand user intent** from natural language queries
2. **Extract required parameters** from the user's request
3. **Ask for missing information** when needed
4. **Execute the appropriate tool** with the correct parameters
5. **Return structured responses** in JSON format

## Response Format

The agent returns responses in this JSON format:

```json
{
  "action": "create_task",
  "payload": "{\"title\": \"Fix login bug\", \"priority\": \"high\"}",
  "missing_fields": ["description"],
  "ask_user": "What is the description for this task?",
  "confirmation_message": null
}
```

Or when all data is available:

```json
{
  "action": "create_task",
  "payload": "{\"title\": \"Fix login bug\", \"description\": \"Login form broken\", \"priority\": \"high\"}",
  "missing_fields": [],
  "ask_user": null,
  "confirmation_message": "✅ Task 'Fix login bug' has been created successfully!"
}
```

## Best Practices

1. **Always validate input**: The agent asks for missing required fields
2. **Use descriptive messages**: Confirmation messages are user-friendly
3. **Handle errors gracefully**: Tools return structured error responses
4. **Filter appropriately**: Use list tools with filters for better performance
5. **Maintain consistency**: Use standard status values and priority levels
