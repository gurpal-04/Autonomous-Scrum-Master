import json
import requests
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# Pydantic models for LLM/Agent understanding and documentation
class TaskCreate(BaseModel):
    title: str = Field(description="Title of the task")
    description: str = Field(description="Description of the task")
    priority: str = Field(description="Priority level (low, medium, high, critical)")
    status: str = Field(description="Current status (todo, in_progress, review, done)")
    story_id: Optional[str] = Field(default=None, description="Associated user story ID")
    epic_id: Optional[str] = Field(default=None, description="Associated epic ID")
    estimated_hours: Optional[float] = Field(default=None, description="Estimated hours to complete")
    assignee_id: Optional[str] = Field(default=None, description="Developer ID to assign")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Title of the task")
    description: Optional[str] = Field(default=None, description="Description of the task")
    priority: Optional[str] = Field(default=None, description="Priority level")
    status: Optional[str] = Field(default=None, description="Current status")
    estimated_hours: Optional[float] = Field(default=None, description="Estimated hours")
    assignee_id: Optional[str] = Field(default=None, description="Developer ID to assign")


class StoryCreate(BaseModel):
    title: str = Field(description="Title of the user story")
    description: str = Field(description="Description of the user story")
    acceptance_criteria: List[str] = Field(description="List of acceptance criteria")
    priority: str = Field(description="Priority level (low, medium, high, critical)")
    status: str = Field(description="Current status (backlog, in_progress, review, done)")
    epic_id: Optional[str] = Field(default=None, description="Associated epic ID")
    story_points: Optional[int] = Field(default=None, description="Story points estimation")
    assignee_id: Optional[str] = Field(default=None, description="Developer ID to assign")


class StoryUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Title of the user story")
    description: Optional[str] = Field(default=None, description="Description of the user story")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="List of acceptance criteria")
    priority: Optional[str] = Field(default=None, description="Priority level")
    status: Optional[str] = Field(default=None, description="Current status")
    story_points: Optional[int] = Field(default=None, description="Story points estimation")
    assignee_id: Optional[str] = Field(default=None, description="Developer ID to assign")


class EpicCreate(BaseModel):
    title: str = Field(description="Title of the epic")
    description: str = Field(description="Description of the epic")
    priority: str = Field(description="Priority level (low, medium, high, critical)")
    status: str = Field(description="Current status (planning, active, completed)")


class EpicUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Title of the epic")
    description: Optional[str] = Field(default=None, description="Description of the epic")
    priority: Optional[str] = Field(default=None, description="Priority level")
    status: Optional[str] = Field(default=None, description="Current status")
    stories: Optional[List[str]] = Field(default=None, description="List of story IDs associated with this epic")


class DeveloperCreate(BaseModel):
    name: str = Field(description="Full name of the developer")
    email: str = Field(description="Email address")
    skills: List[str] = Field(description="List of technical skills")
    availability: str = Field(description="Availability status (available, busy, unavailable)")


class DeveloperUpdate(BaseModel):
    name: Optional[str] = Field(default=None, description="Full name of the developer")
    email: Optional[str] = Field(default=None, description="Email address")
    skills: Optional[List[str]] = Field(default=None, description="List of technical skills")
    availability: Optional[str] = Field(default=None, description="Availability status")


class EpicDecompose(BaseModel):
    epic_id: str = Field(description="The ID of the existing epic to decompose")
    constraints: Optional[List[str]] = Field(default=None, description="List of constraints for the epic")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="List of acceptance criteria for the epic")


class StoryDecompose(BaseModel):
    story_description: str = Field(description="Description of the user story to decompose")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="List of acceptance criteria for the story")
    constraints: Optional[List[str]] = Field(default=None, description="List of constraints for the story")


class EpicCreateAndDecompose(BaseModel):
    title: str = Field(description="Title of the new epic to create and decompose")
    description: str = Field(description="Description of the new epic")
    constraints: Optional[List[str]] = Field(default=None, description="List of constraints for the epic")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="List of acceptance criteria for the epic")


# Base URL for the API
BASE_URL = "http://localhost:8080"  # Adjust this based on your deployment


def create_task(title: str, description: str, priority: str, status: str = "todo", 
                story_id: Optional[str] = None, epic_id: Optional[str] = None, 
                estimated_hours: Optional[float] = None, assignee_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new task with the specified details.
    
    Args:
        title: Title of the task
        description: Description of the task
        priority: Priority level (low, medium, high, critical)
        status: Current status (default: todo)
        story_id: Associated user story ID (optional)
        epic_id: Associated epic ID (optional)
        estimated_hours: Estimated hours to complete (optional)
        assignee_id: Developer ID to assign (optional)
    
    Returns:
        Dictionary containing the task ID and success message
    """
    try:
        task_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": status
        }
        
        if story_id:
            task_data["story_id"] = story_id
        if epic_id:
            task_data["epic_id"] = epic_id
        if estimated_hours:
            task_data["estimated_hours"] = estimated_hours
        if assignee_id:
            task_data["assignee_id"] = assignee_id
            
        response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "task_id": result.get("id"),
            "message": result.get("message", "Task created successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to create task: {str(e)}"
        }


def list_tasks(status: Optional[str] = None, assignee_id: Optional[str] = None, 
               epic_id: Optional[str] = None, priority: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all tasks with optional filtering.
    
    Args:
        status: Filter by status (optional)
        assignee_id: Filter by assigned developer (optional)
        epic_id: Filter by epic ID (optional)
        priority: Filter by priority (optional)
    
    Returns:
        Dictionary containing the list of tasks
    """
    try:
        params = {}
        if status:
            params["status"] = status
        if assignee_id:
            params["assignee_id"] = assignee_id
        if epic_id:
            params["epic_id"] = epic_id
        if priority:
            params["priority"] = priority
            
        response = requests.get(f"{BASE_URL}/tasks/", params=params)
        response.raise_for_status()
        
        tasks = response.json()
        return {
            "status": "success",
            "tasks": tasks,
            "count": len(tasks)
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to list tasks: {str(e)}"
        }


def get_task(task_id: str) -> Dict[str, Any]:
    """
    Retrieves a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
    
    Returns:
        Dictionary containing the task details
    """
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        response.raise_for_status()
        
        task = response.json()
        return {
            "status": "success",
            "task": task
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to get task: {str(e)}"
        }


def update_task(task_id: str, **updates) -> Dict[str, Any]:
    """
    Updates a task with the specified changes.
    
    Args:
        task_id: The ID of the task to update
        **updates: Fields to update (title, description, priority, status, estimated_hours, assignee_id)
    
    Returns:
        Dictionary containing the update result
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in updates.items() if v is not None}
        
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Task updated successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to update task: {str(e)}"
        }


def delete_task(task_id: str) -> Dict[str, Any]:
    """
    Deletes a task by ID.
    
    Args:
        task_id: The ID of the task to delete
    
    Returns:
        Dictionary containing the deletion result
    """
    try:
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Task deleted successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete task: {str(e)}"
        }


def assign_developers_to_task(task_id: str, developer_ids: List[str]) -> Dict[str, Any]:
    """
    Assigns developers to a task.
    
    Args:
        task_id: The ID of the task
        developer_ids: List of developer IDs to assign
    
    Returns:
        Dictionary containing the assignment result
    """
    try:
        assignment_data = {"developer_ids": developer_ids}
        response = requests.post(f"{BASE_URL}/tasks/{task_id}/assign", json=assignment_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Developers assigned successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to assign developers: {str(e)}"
        }


def create_epic(title: str, description: str, priority: str, status: str = "planning") -> Dict[str, Any]:
    """
    Creates a new epic with the specified details.
    
    Args:
        title: Title of the epic
        description: Description of the epic
        priority: Priority level (low, medium, high, critical)
        status: Current status (default: planning)
    
    Returns:
        Dictionary containing the epic ID and success message
    """
    try:
        epic_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": status
        }
        
        response = requests.post(f"{BASE_URL}/epic/", json=epic_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "epic_id": result.get("id"),
            "message": "Epic created successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to create epic: {str(e)}"
        }


def list_epics() -> Dict[str, Any]:
    """
    Lists all epics.
    
    Returns:
        Dictionary containing the list of epics
    """
    try:
        response = requests.get(f"{BASE_URL}/epic/")
        response.raise_for_status()
        
        epics = response.json()
        return {
            "status": "success",
            "epics": epics,
            "count": len(epics)
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to list epics: {str(e)}"
        }


def get_epic(epic_id: str) -> Dict[str, Any]:
    """
    Retrieves a specific epic by ID.
    
    Args:
        epic_id: The ID of the epic to retrieve
    
    Returns:
        Dictionary containing the epic details
    """
    try:
        response = requests.get(f"{BASE_URL}/epic/{epic_id}")
        response.raise_for_status()
        
        epic = response.json()
        return {
            "status": "success",
            "epic": epic
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to get epic: {str(e)}"
        }


def update_epic(epic_id: str, **updates) -> Dict[str, Any]:
    """
    Updates an epic with the specified changes.
    
    Args:
        epic_id: The ID of the epic to update
        **updates: Fields to update (title, description, priority, status)
    
    Returns:
        Dictionary containing the update result
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in updates.items() if v is not None}
        
        response = requests.put(f"{BASE_URL}/epic/{epic_id}", json=update_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": "Epic updated successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to update epic: {str(e)}"
        }


def create_developer(name: str, email: str, skills: List[str], availability: str = "available") -> Dict[str, Any]:
    """
    Creates a new developer profile.
    
    Args:
        name: Full name of the developer
        email: Email address
        skills: List of technical skills
        availability: Availability status (default: available)
    
    Returns:
        Dictionary containing the developer ID and success message
    """
    try:
        developer_data = {
            "name": name,
            "email": email,
            "skills": skills,
            "availability": availability
        }
        
        response = requests.post(f"{BASE_URL}/developers/", json=developer_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "developer_id": result.get("id"),
            "message": result.get("message", "Developer created successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to create developer: {str(e)}"
        }


def list_developers() -> Dict[str, Any]:
    """
    Lists all developers.
    
    Returns:
        Dictionary containing the list of developers
    """
    try:
        response = requests.get(f"{BASE_URL}/developers/")
        response.raise_for_status()
        
        developers = response.json()
        return {
            "status": "success",
            "developers": developers,
            "count": len(developers)
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to list developers: {str(e)}"
        }


def get_developer(developer_id: str) -> Dict[str, Any]:
    """
    Retrieves a specific developer by ID.
    
    Args:
        developer_id: The ID of the developer to retrieve
    
    Returns:
        Dictionary containing the developer details
    """
    try:
        response = requests.get(f"{BASE_URL}/developers/{developer_id}")
        response.raise_for_status()
        
        developer = response.json()
        return {
            "status": "success",
            "developer": developer
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to get developer: {str(e)}"
        }


def update_developer(developer_id: str, **updates) -> Dict[str, Any]:
    """
    Updates a developer profile with the specified changes.
    
    Args:
        developer_id: The ID of the developer to update
        **updates: Fields to update (name, email, skills, availability)
    
    Returns:
        Dictionary containing the update result
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in updates.items() if v is not None}
        
        response = requests.put(f"{BASE_URL}/developers/{developer_id}", json=update_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Developer updated successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to update developer: {str(e)}"
        }


def delete_developer(developer_id: str) -> Dict[str, Any]:
    """
    Deletes a developer profile by ID.
    
    Args:
        developer_id: The ID of the developer to delete
    
    Returns:
        Dictionary containing the deletion result
    """
    try:
        response = requests.delete(f"{BASE_URL}/developers/{developer_id}")
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Developer deleted successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete developer: {str(e)}"
        }


def decompose_epic_to_stories(epic_id: str) -> Dict[str, Any]:
    """
    Decomposes an existing epic into user stories using AI.
    
    Args:
        epic_id: The ID of the existing epic to decompose
    
    Returns:
        Dictionary containing the epic ID and created stories
    """
    try:
        # First get the epic details
        epic_response = requests.get(f"{BASE_URL}/epic/{epic_id}")
        epic_response.raise_for_status()
        epic_data = epic_response.json()
        
        decompose_data = {
            "title": epic_data.get("title"),
            "description": epic_data.get("description"),
            "epic_id": epic_id
        }
            
        response = requests.post(f"{BASE_URL}/epic/decompose", json=decompose_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "epic_id": epic_id,
            "stories": result.get("stories", []),
            "message": f"Epic '{epic_data.get('title')}' decomposed into {len(result.get('stories', []))} stories"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to decompose epic: {str(e)}"
        }


def decompose_story_to_tasks(story_description: str, acceptance_criteria: Optional[List[str]] = None, 
                            constraints: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Decomposes a user story into tasks using AI.
    
    Args:
        story_description: Description of the user story to decompose
    
    Returns:
        Dictionary containing the decomposition result
    """
    try:
        decompose_data = {
            "story_description": story_description
        }
            
        response = requests.post(f"{BASE_URL}/user_story/decompose", json=decompose_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "response": result.get("response"),
            "message": "User story decomposed into tasks successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to decompose user story: {str(e)}"
        }


def create_and_decompose_epic(title: str, description: str, constraints: Optional[List[str]] = None, 
                             acceptance_criteria: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Creates a new epic and immediately decomposes it into user stories using AI.
    
    Args:
        title: Title of the new epic
        description: Description of the new epic
    
    Returns:
        Dictionary containing the epic ID and created stories
    """
    try:
        decompose_data = {
            "title": title,
            "description": description
        }
        
        if constraints:
            decompose_data["constraints"] = constraints
        if acceptance_criteria:
            decompose_data["acceptance_criteria"] = acceptance_criteria
            
        response = requests.post(f"{BASE_URL}/epic/decompose", json=decompose_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "epic_id": result.get("epic_id"),
            "stories": result.get("stories", []),
            "message": f"New epic '{title}' created and decomposed into {len(result.get('stories', []))} stories"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to create and decompose epic: {str(e)}"
        }


def find_epic_by_title(title: str) -> Dict[str, Any]:
    """
    Finds an epic by its title and returns its ID.
    
    Args:
        title: The title of the epic to find
    
    Returns:
        Dictionary containing the epic ID if found, or error message
    """
    try:
        response = requests.get(f"{BASE_URL}/epic/")
        response.raise_for_status()
        
        epics = response.json()
        
        # Search for epic with matching title (case-insensitive)
        for epic in epics:
            if epic.get("title", "").lower() == title.lower():
                return {
                    "status": "success",
                    "epic_id": epic.get("id"),
                    "epic": epic
                }
        
        return {
            "status": "error",
            "error_message": f"No epic found with title '{title}'"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for epic: {str(e)}"
        }


def create_story(title: str, description: str, acceptance_criteria: List[str], priority: str, 
                 status: str = "backlog", epic_id: Optional[str] = None, 
                 story_points: Optional[int] = None, assignee_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a new user story with the specified details.
    
    Args:
        title: Title of the user story
        description: Description of the user story
        acceptance_criteria: List of acceptance criteria
        priority: Priority level (low, medium, high, critical)
        status: Current status (default: backlog)
        epic_id: Associated epic ID (optional)
        story_points: Story points estimation (optional)
        assignee_id: Developer ID to assign (optional)
    
    Returns:
        Dictionary containing the story ID and success message
    """
    try:
        story_data = {
            "title": title,
            "description": description,
            "acceptance_criteria": acceptance_criteria,
            "priority": priority,
            "status": status
        }
        
        if epic_id:
            story_data["epic_id"] = epic_id
        if story_points:
            story_data["story_points"] = story_points
        if assignee_id:
            story_data["assignee_id"] = assignee_id
            
        response = requests.post(f"{BASE_URL}/user_story/", json=story_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "story_id": result.get("id"),
            "message": result.get("message", "User story created successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to create user story: {str(e)}"
        }


def list_stories(status: Optional[str] = None, assignee_id: Optional[str] = None, 
                epic_id: Optional[str] = None, priority: Optional[str] = None) -> Dict[str, Any]:
    """
    Lists all user stories with optional filtering.
    
    Args:
        status: Filter by status (optional)
        assignee_id: Filter by assigned developer (optional)
        epic_id: Filter by epic ID (optional)
        priority: Filter by priority (optional)
    
    Returns:
        Dictionary containing the list of user stories
    """
    try:
        params = {}
        if status:
            params["status"] = status
        if assignee_id:
            params["assignee_id"] = assignee_id
        if epic_id:
            params["epic_id"] = epic_id
        if priority:
            params["priority"] = priority
            
        response = requests.get(f"{BASE_URL}/user_story/", params=params)
        response.raise_for_status()
        
        stories = response.json()
        return {
            "status": "success",
            "stories": stories,
            "count": len(stories)
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to list user stories: {str(e)}"
        }


def get_story(story_id: str) -> Dict[str, Any]:
    """
    Retrieves a specific user story by ID.
    
    Args:
        story_id: The ID of the user story to retrieve
    
    Returns:
        Dictionary containing the user story details
    """
    try:
        response = requests.get(f"{BASE_URL}/user_story/{story_id}")
        response.raise_for_status()
        
        story = response.json()
        return {
            "status": "success",
            "story": story
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to get user story: {str(e)}"
        }


def update_story(story_id: str, **updates) -> Dict[str, Any]:
    """
    Updates a user story with the specified changes.
    
    Args:
        story_id: The ID of the user story to update
        **updates: Fields to update (title, description, acceptance_criteria, priority, status, story_points, assignee_id)
    
    Returns:
        Dictionary containing the update result
    """
    try:
        # Filter out None values
        update_data = {k: v for k, v in updates.items() if v is not None}
        
        response = requests.put(f"{BASE_URL}/user_story/{story_id}", json=update_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "User story updated successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to update user story: {str(e)}"
        }


def delete_story(story_id: str) -> Dict[str, Any]:
    """
    Deletes a user story by ID.
    
    Args:
        story_id: The ID of the user story to delete
    
    Returns:
        Dictionary containing the deletion result
    """
    try:
        response = requests.delete(f"{BASE_URL}/user_story/{story_id}")
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "User story deleted successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to delete user story: {str(e)}"
        }


def assign_developers_to_story(story_id: str, developer_ids: List[str]) -> Dict[str, Any]:
    """
    Assigns developers to a user story.
    
    Args:
        story_id: The ID of the user story
        developer_ids: List of developer IDs to assign
    
    Returns:
        Dictionary containing the assignment result
    """
    try:
        assignment_data = {"developer_ids": developer_ids}
        response = requests.post(f"{BASE_URL}/user_story/{story_id}/assign", json=assignment_data)
        response.raise_for_status()
        
        result = response.json()
        return {
            "status": "success",
            "message": result.get("message", "Developers assigned to story successfully")
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to assign developers to story: {str(e)}"
        }


def find_story_by_title(title: str) -> Dict[str, Any]:
    """
    Finds a user story by its title and returns its ID.
    
    Args:
        title: The title of the user story to find
    
    Returns:
        Dictionary containing the story ID if found, or error message
    """
    try:
        response = requests.get(f"{BASE_URL}/user_story/")
        response.raise_for_status()
        
        stories = response.json()
        
        # Search for story with matching title (case-insensitive)
        for story in stories:
            if story.get("title", "").lower() == title.lower():
                return {
                    "status": "success",
                    "story_id": story.get("id"),
                    "story": story
                }
        
        return {
            "status": "error",
            "error_message": f"No user story found with title '{title}'"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for user story: {str(e)}"
        } 