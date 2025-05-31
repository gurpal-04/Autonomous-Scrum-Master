from firestore import task

# Create task
task_id = task.create_task({
    "title": "Implement Sprint Planner Agent",
    "status": "open",
    "assignee": "saurabh"
})

# Add comment
task.add_comment(task_id, {
    "author": "saurabh",
    "message": "Started initial testing of the planner."
})

# Log activity
task.log_activity(task_id, {
    "actor": "saurabh",
    "action": "Task created"
})

# Fetch everything
print("Task:", task.get_task(task_id))
print("Comments:", task.get_comments(task_id))
print("Activity:", task.get_activity_log(task_id))
