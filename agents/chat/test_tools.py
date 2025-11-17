#!/usr/bin/env python3
"""
Test script to demonstrate the function tools for the chat agent.
This script shows how the tools can be used to perform various Scrum operations.
"""

import json
from tools import (
    create_task, list_tasks, get_task, update_task, delete_task, assign_developers_to_task,
    create_epic, list_epics, get_epic, update_epic,
    create_developer, list_developers, get_developer, update_developer, delete_developer
)


def test_task_operations():
    """Test task-related operations."""
    print("=== Testing Task Operations ===")
    
    # Create a task
    print("\n1. Creating a task...")
    result = create_task(
        title="Fix login bug",
        description="The login form is not working properly on mobile devices",
        priority="high",
        status="todo",
        estimated_hours=4.0
    )
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if result["status"] == "success":
        task_id = result["task_id"]
        
        # Get the task
        print(f"\n2. Getting task {task_id}...")
        result = get_task(task_id)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Update the task
        print(f"\n3. Updating task {task_id}...")
        result = update_task(task_id, status="in_progress", estimated_hours=6.0)
        print(f"Result: {json.dumps(result, indent=2)}")
    
    # List all tasks
    print("\n4. Listing all tasks...")
    result = list_tasks()
    print(f"Result: {json.dumps(result, indent=2)}")


def test_epic_operations():
    """Test epic-related operations."""
    print("\n=== Testing Epic Operations ===")
    
    # Create an epic
    print("\n1. Creating an epic...")
    result = create_epic(
        title="User Authentication System",
        description="Implement a complete user authentication system with OAuth support",
        priority="critical",
        status="planning"
    )
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if result["status"] == "success":
        epic_id = result["epic_id"]
        
        # Get the epic
        print(f"\n2. Getting epic {epic_id}...")
        result = get_epic(epic_id)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Update the epic
        print(f"\n3. Updating epic {epic_id}...")
        result = update_epic(epic_id, status="active")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    # List all epics
    print("\n4. Listing all epics...")
    result = list_epics()
    print(f"Result: {json.dumps(result, indent=2)}")


def test_developer_operations():
    """Test developer-related operations."""
    print("\n=== Testing Developer Operations ===")
    
    # Create a developer
    print("\n1. Creating a developer...")
    result = create_developer(
        name="John Doe",
        email="john.doe@example.com",
        skills=["Python", "JavaScript", "React", "FastAPI"],
        availability="available"
    )
    print(f"Result: {json.dumps(result, indent=2)}")
    
    if result["status"] == "success":
        developer_id = result["developer_id"]
        
        # Get the developer
        print(f"\n2. Getting developer {developer_id}...")
        result = get_developer(developer_id)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # Update the developer
        print(f"\n3. Updating developer {developer_id}...")
        result = update_developer(developer_id, availability="busy")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    # List all developers
    print("\n4. Listing all developers...")
    result = list_developers()
    print(f"Result: {json.dumps(result, indent=2)}")


def test_developer_assignment():
    """Test developer assignment to tasks."""
    print("\n=== Testing Developer Assignment ===")
    
    # First create a developer
    print("\n1. Creating a developer for assignment...")
    dev_result = create_developer(
        name="Jane Smith",
        email="jane.smith@example.com",
        skills=["Python", "Django", "PostgreSQL"],
        availability="available"
    )
    
    if dev_result["status"] == "success":
        developer_id = dev_result["developer_id"]
        
        # Create a task
        print("\n2. Creating a task for assignment...")
        task_result = create_task(
            title="Database optimization",
            description="Optimize database queries for better performance",
            priority="medium",
            status="todo"
        )
        
        if task_result["status"] == "success":
            task_id = task_result["task_id"]
            
            # Assign developer to task
            print(f"\n3. Assigning developer {developer_id} to task {task_id}...")
            result = assign_developers_to_task(task_id, [developer_id])
            print(f"Result: {json.dumps(result, indent=2)}")
            
            # List tasks with the assigned developer
            print(f"\n4. Listing tasks assigned to developer {developer_id}...")
            result = list_tasks(assignee_id=developer_id)
            print(f"Result: {json.dumps(result, indent=2)}")


def main():
    """Run all tests."""
    print("Starting function tools test...")
    print("Note: Make sure your API server is running on http://localhost:8080")
    
    try:
        test_task_operations()
        test_epic_operations()
        test_developer_operations()
        test_developer_assignment()
        
        print("\n=== All tests completed! ===")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("Make sure your API server is running and accessible.")


if __name__ == "__main__":
    main() 