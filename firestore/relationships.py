# from firebase_admin import firestore
from typing import List, Dict, Optional
from datetime import datetime, timezone
from firestore.firestore_client import db
from google.cloud import firestore

# Type definitions for better code clarity
EpicId = str
StoryId = str
TaskId = str

class CircularDependencyError(Exception):
    """Raised when a task dependency would create a circular reference."""
    pass

class EntityNotFoundError(Exception):
    """Raised when a referenced entity (epic, story, or task) is not found."""
    pass

# ---------- Epic-Story Relationships ----------

def link_story_to_epic(story_id: StoryId, epic_id: EpicId) -> None:
    """
    Link a story to an epic (bidirectional relationship).
    
    Args:
        story_id: ID of the story to link
        epic_id: ID of the epic to link to
        
    Raises:
        EntityNotFoundError: If either story or epic doesn't exist
    """
    # Verify both documents exist
    story_doc = db.collection("stories").document(story_id).get()
    epic_doc = db.collection("epics").document(epic_id).get()
    
    if not story_doc.exists:
        raise EntityNotFoundError(f"Story {story_id} does not exist")
    if not epic_doc.exists:
        raise EntityNotFoundError(f"Epic {epic_id} does not exist")
    
    # Get references
    epic_ref = db.collection("epics").document(epic_id)
    story_ref = db.collection("stories").document(story_id)
    
    # Update both documents
    epic_ref.update({
        "stories": firestore.ArrayUnion([story_id])
    })
    
    story_ref.update({
        "epic_id": epic_id,
        "updated_at": datetime.now(timezone.utc)
    })

def unlink_story_from_epic(story_id: StoryId, epic_id: EpicId) -> None:
    """
    Remove the link between a story and its epic.
    
    Args:
        story_id: ID of the story to unlink
        epic_id: ID of the epic to unlink from
    """
    # Get references
    epic_ref = db.collection("epics").document(epic_id)
    story_ref = db.collection("stories").document(story_id)
    
    # Update both documents
    epic_ref.update({
        "stories": firestore.ArrayRemove([story_id])
    })
    
    story_ref.update({
        "epic_id": firestore.DELETE_FIELD,
        "updated_at": datetime.now(timezone.utc)
    })

def get_epic_stories(epic_id: EpicId) -> List[Dict]:
    """
    Get all stories associated with an epic.
    
    Args:
        epic_id: ID of the epic
        
    Returns:
        List of story documents with their IDs
    """
    epic = db.collection("epics").document(epic_id).get()
    if not epic.exists:
        return []
    
    epic_data = epic.to_dict()
    story_ids = epic_data.get("stories", [])
    
    stories = []
    for story_id in story_ids:
        story = db.collection("stories").document(story_id).get()
        if story.exists:
            story_data = story.to_dict()
            story_data["id"] = story.id
            stories.append(story_data)
    return stories

def bulk_link_stories_to_epic(story_ids: List[StoryId], epic_id: EpicId) -> None:
    """
    Link multiple stories to an epic in a single batch operation.
    
    Args:
        story_ids: List of story IDs to link
        epic_id: ID of the epic to link to
    """
    # Verify epic exists
    epic_doc = db.collection("epics").document(epic_id).get()
    if not epic_doc.exists:
        raise EntityNotFoundError(f"Epic {epic_id} does not exist")
    
    # Verify all stories exist
    stories_ref = db.collection("stories")
    for story_id in story_ids:
        if not stories_ref.document(story_id).get().exists:
            raise EntityNotFoundError(f"Story {story_id} does not exist")
    
    # Create batch operation
    batch = db.batch()
    
    # Update epic with all story IDs
    epic_ref = db.collection("epics").document(epic_id)
    batch.update(epic_ref, {
        "stories": firestore.ArrayUnion(story_ids)
    })
    
    # Update all stories with epic ID
    current_time = datetime.now(timezone.utc)
    for story_id in story_ids:
        story_ref = stories_ref.document(story_id)
        batch.update(story_ref, {
            "epic_id": epic_id,
            "updated_at": current_time
        })
    
    # Execute the batch
    batch.commit()

# ---------- Story-Task Relationships ----------

def link_task_to_story(task_id: TaskId, story_id: StoryId) -> None:
    """
    Link a task to a story (bidirectional relationship).
    
    Args:
        task_id: ID of the task to link
        story_id: ID of the story to link to
        
    Raises:
        EntityNotFoundError: If either task or story doesn't exist
    """
    # Verify both documents exist
    story_doc = db.collection("stories").document(story_id).get()
    task_doc = db.collection("tasks").document(task_id).get()
    
    if not story_doc.exists:
        raise EntityNotFoundError(f"Story {story_id} does not exist")
    if not task_doc.exists:
        raise EntityNotFoundError(f"Task {task_id} does not exist")
    
    # Get references
    story_ref = db.collection("stories").document(story_id)
    task_ref = db.collection("tasks").document(task_id)
    
    # Update both documents
    story_ref.update({
        "tasks": firestore.ArrayUnion([task_id]),
        "updated_at": datetime.now(timezone.utc)
    })
    
    task_ref.update({
        "story_id": story_id,
        "updated_at": datetime.now(timezone.utc)
    })

def unlink_task_from_story(task_id: TaskId, story_id: StoryId) -> None:
    """
    Remove the link between a task and its story.
    
    Args:
        task_id: ID of the task to unlink
        story_id: ID of the story to unlink from
    """
    # Get references
    story_ref = db.collection("stories").document(story_id)
    task_ref = db.collection("tasks").document(task_id)
    
    # Update both documents
    story_ref.update({
        "tasks": firestore.ArrayRemove([task_id]),
        "updated_at": datetime.now(timezone.utc)
    })
    
    task_ref.update({
        "story_id": firestore.DELETE_FIELD,
        "updated_at": datetime.now(timezone.utc)
    })

def get_story_tasks(story_id: StoryId) -> List[Dict]:
    """
    Get all tasks associated with a story.
    
    Args:
        story_id: ID of the story
        
    Returns:
        List of task documents with their IDs
    """
    story = db.collection("stories").document(story_id).get()
    if not story.exists:
        return []
    
    story_data = story.to_dict()
    task_ids = story_data.get("tasks", [])
    
    tasks = []
    for task_id in task_ids:
        task = db.collection("tasks").document(task_id).get()
        if task.exists:
            task_data = task.to_dict()
            task_data["id"] = task.id
            tasks.append(task_data)
    return tasks

# ---------- Task Dependencies ----------

def has_circular_dependency(task_id: TaskId, depends_on_task_id: TaskId, visited: Optional[set] = None) -> bool:
    """
    Check if adding a dependency would create a circular reference.
    
    Args:
        task_id: ID of the task to check
        depends_on_task_id: ID of the task that would be added as a dependency
        visited: Set of already visited task IDs (used for recursion)
        
    Returns:
        True if adding the dependency would create a circular reference
    """
    if visited is None:
        visited = set()
    
    if task_id in visited:
        return True
    
    visited.add(task_id)
    task = db.collection("tasks").document(task_id).get()
    if not task.exists:
        return False
    
    task_data = task.to_dict()
    dependencies = task_data.get("dependencies", [])
    
    for dep_id in dependencies:
        if has_circular_dependency(dep_id, depends_on_task_id, visited):
            return True
    
    return False

def add_task_dependency(task_id: TaskId, depends_on_task_id: TaskId) -> None:
    """
    Make a task dependent on another task.
    
    Args:
        task_id: ID of the task that will depend on another
        depends_on_task_id: ID of the task that will be depended upon
        
    Raises:
        CircularDependencyError: If adding this dependency would create a circular reference
        EntityNotFoundError: If either task doesn't exist
    """
    # Check if tasks exist
    task = db.collection("tasks").document(task_id).get()
    depends_on_task = db.collection("tasks").document(depends_on_task_id).get()
    
    if not task.exists:
        raise EntityNotFoundError(f"Task {task_id} does not exist")
    if not depends_on_task.exists:
        raise EntityNotFoundError(f"Task {depends_on_task_id} does not exist")
    
    # Check for circular dependencies
    if has_circular_dependency(depends_on_task_id, task_id):
        raise CircularDependencyError(
            f"Adding dependency from {task_id} to {depends_on_task_id} would create a circular reference"
        )
    
    # Add the dependency
    task_ref = db.collection("tasks").document(task_id)
    task_ref.update({
        "dependencies": firestore.ArrayUnion([depends_on_task_id]),
        "updated_at": datetime.now(timezone.utc)
    })

def remove_task_dependency(task_id: TaskId, depends_on_task_id: TaskId) -> None:
    """
    Remove a dependency between tasks.
    
    Args:
        task_id: ID of the task that depends on another
        depends_on_task_id: ID of the task that is depended upon
    """
    task_ref = db.collection("tasks").document(task_id)
    task_ref.update({
        "dependencies": firestore.ArrayRemove([depends_on_task_id]),
        "updated_at": datetime.now(timezone.utc)
    })

def get_task_dependencies(task_id: TaskId) -> List[Dict]:
    """
    Get all dependencies for a task.
    
    Args:
        task_id: ID of the task
        
    Returns:
        List of task documents that this task depends on
    """
    task = db.collection("tasks").document(task_id).get()
    if not task.exists:
        return []
    
    task_data = task.to_dict()
    dependency_ids = task_data.get("dependencies", [])
    
    dependencies = []
    for dep_id in dependency_ids:
        dep = db.collection("tasks").document(dep_id).get()
        if dep.exists:
            dep_data = dep.to_dict()
            dep_data["id"] = dep.id
            dependencies.append(dep_data)
    return dependencies

def get_dependent_tasks(task_id: TaskId) -> List[Dict]:
    """
    Get all tasks that depend on this task.
    
    Args:
        task_id: ID of the task
        
    Returns:
        List of task documents that depend on this task
    """
    # Query for tasks that have this task in their dependencies array
    dependent_tasks = db.collection("tasks").where("dependencies", "array_contains", task_id).stream()
    
    return [
        task.to_dict() | {"id": task.id}
        for task in dependent_tasks
    ] 