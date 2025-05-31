from firestore import relationships
from firestore import epic, story, task
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS: test", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# ---------- EPIC-STORY RELATIONSHIPS ----------
print("\n=== Testing Epic-Story Relationships ===")

# Create test data
epic_data = {
    "title": "User Management",
    "description": "Implement user management features",
    "status": "in-progress",
    "created_at": datetime.utcnow()
}

story_data = {
    "title": "User Registration",
    "description": "Implement user registration flow",
    "status": "todo",
    "created_at": datetime.utcnow()
}

# Create epic and story
epic_id = epic.create_epic(epic_data)
story_id = story.create_story(story_data)
print(f"[+] Created epic with ID: {epic_id}")
print(f"[+] Created story with ID: {story_id}")

# Link story to epic
relationships.link_story_to_epic(story_id, epic_id)
print(f"[+] Linked story {story_id} to epic {epic_id}")

# Verify the link
epic_stories = relationships.get_epic_stories(epic_id)
print(f"[✓] Epic stories: {epic_stories}")

# Unlink story from epic
relationships.unlink_story_from_epic(story_id, epic_id)
print(f"[-] Unlinked story from epic")

# Verify unlink
epic_stories = relationships.get_epic_stories(epic_id)
print(f"[✓] Epic stories after unlink: {epic_stories}")

# Cleanup
epic.delete_epic(epic_id)
story.delete_story(story_id)
print(f"[✓] Cleaned up epic and story")

# ---------- STORY-TASK RELATIONSHIPS ----------
print("\n=== Testing Story-Task Relationships ===")

# Create test data
story_data = {
    "title": "User Login",
    "description": "Implement user login functionality",
    "status": "todo",
    "created_at": datetime.utcnow()
}

task_data = {
    "title": "Implement Login API",
    "description": "Create REST endpoint for user login",
    "status": "open",
    "created_at": datetime.utcnow()
}

# Create story and task
story_id = story.create_story(story_data)
task_id = task.create_task(task_data)
print(f"[+] Created story with ID: {story_id}")
print(f"[+] Created task with ID: {task_id}")

# Link task to story
relationships.link_task_to_story(task_id, story_id)
print(f"[+] Linked task {task_id} to story {story_id}")

# Verify the link
story_tasks = relationships.get_story_tasks(story_id)
print(f"[✓] Story tasks: {story_tasks}")

# Unlink task from story
relationships.unlink_task_from_story(task_id, story_id)
print(f"[-] Unlinked task from story")

# Verify unlink
story_tasks = relationships.get_story_tasks(story_id)
print(f"[✓] Story tasks after unlink: {story_tasks}")

# Cleanup
story.delete_story(story_id)
task.delete_task(task_id)
print(f"[✓] Cleaned up story and task")

# ---------- TASK DEPENDENCIES ----------
print("\n=== Testing Task Dependencies ===")

# Create test tasks
task1_data = {
    "title": "Setup Database",
    "description": "Setup and configure database",
    "status": "open",
    "created_at": datetime.utcnow()
}

task2_data = {
    "title": "Create Tables",
    "description": "Create database tables",
    "status": "open",
    "created_at": datetime.utcnow()
}

# Create tasks
task1_id = task.create_task(task1_data)
task2_id = task.create_task(task2_data)
print(f"[+] Created task1 with ID: {task1_id}")
print(f"[+] Created task2 with ID: {task2_id}")

# Add dependency
relationships.add_task_dependency(task2_id, task1_id)  # task2 depends on task1
print(f"[+] Added dependency: task2 depends on task1")

# Verify dependency
dependencies = relationships.get_task_dependencies(task2_id)
print(f"[✓] Task2 dependencies: {dependencies}")

dependent_tasks = relationships.get_dependent_tasks(task1_id)
print(f"[✓] Tasks dependent on task1: {dependent_tasks}")

# Remove dependency
relationships.remove_task_dependency(task2_id, task1_id)
print(f"[-] Removed dependency between tasks")

# Verify removal
dependencies = relationships.get_task_dependencies(task2_id)
print(f"[✓] Task2 dependencies after removal: {dependencies}")

# Test circular dependency prevention
try:
    # Create circular dependency (should fail)
    relationships.add_task_dependency(task2_id, task1_id)
    relationships.add_task_dependency(task1_id, task2_id)
except relationships.CircularDependencyError as e:
    print(f"[✓] Successfully prevented circular dependency: {e}")

# Cleanup
task.delete_task(task1_id)
task.delete_task(task2_id)
print(f"[✓] Cleaned up tasks")

# ---------- ERROR HANDLING ----------
print("\n=== Testing Error Handling ===")

# Test with non-existent entities
non_existent_id = "non_existent_id"

try:
    relationships.link_story_to_epic(non_existent_id, non_existent_id)
except relationships.EntityNotFoundError as e:
    print(f"[✓] Successfully caught non-existent story/epic: {e}")

try:
    relationships.add_task_dependency(non_existent_id, non_existent_id)
except relationships.EntityNotFoundError as e:
    print(f"[✓] Successfully caught non-existent task: {e}")

print("\n=== All Tests Completed ===") 