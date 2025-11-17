"""
Test file for the Sprint Tasks API.

This file tests the API endpoint for getting all tasks for a particular sprint.
"""

import requests
import json

def test_get_sprint_tasks():
    """Test getting all tasks for a sprint."""
    print("🧪 Testing GET /sprint/{sprint_id}/tasks API...")
    
    # First, create a sprint with some tasks
    print("\n1. Creating a sprint with tasks...")
    
    # Create sprint plan with tasks
    payload = {
        "tasks": [
            {
                "title": "Implement user authentication",
                "description": "Create login/logout functionality with JWT tokens",
                "role": "backend",
                "estimate_hours": 16,
                "sprint_points": 8
            },
            {
                "title": "Design login page UI",
                "description": "Create responsive login form with validation",
                "role": "frontend", 
                "estimate_hours": 12,
                "sprint_points": 5
            },
            {
                "title": "Write authentication tests",
                "description": "Unit and integration tests for auth flow",
                "role": "qa",
                "estimate_hours": 8,
                "sprint_points": 3
            }
        ],
        "developers": [
            {
                "name": "Alice Johnson",
                "role": "backend",
                "available_hours_per_day": 6
            },
            {
                "name": "Bob Smith", 
                "role": "frontend",
                "available_hours_per_day": 6
            },
            {
                "name": "Carol Davis",
                "role": "qa",
                "available_hours_per_day": 6
            }
        ],
        "timeline_days": 10,
        "sprint_name": "Test Sprint for Tasks API",
        "sprint_goal": "Test the sprint tasks API functionality"
    }
    
    try:
        # Create sprint plan
        response = requests.post(
            "http://localhost:8080/sprint/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            sprint_id = result.get("sprint_id")
            planned_task_ids = result.get("planned_task_ids", [])
            
            print(f"✅ Sprint created successfully!")
            print(f"Sprint ID: {sprint_id}")
            print(f"Planned task IDs: {planned_task_ids}")
            print(f"Number of planned tasks: {len(planned_task_ids)}")
            
            # Now test getting tasks for this sprint
            print(f"\n2. Testing GET /sprint/{sprint_id}/tasks...")
            
            tasks_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
            
            if tasks_response.status_code == 200:
                tasks_result = tasks_response.json()
                tasks = tasks_result.get("tasks", [])
                
                print(f"✅ Retrieved tasks successfully!")
                print(f"Number of tasks returned: {len(tasks)}")
                print(f"Expected number of tasks: {len(planned_task_ids)}")
                
                # Verify that we got the expected number of tasks
                if len(tasks) == len(planned_task_ids):
                    print("✅ Task count matches expected!")
                else:
                    print(f"❌ Task count mismatch! Expected {len(planned_task_ids)}, got {len(tasks)}")
                
                # Display task details
                print(f"\nTask details:")
                for i, task in enumerate(tasks, 1):
                    print(f"  {i}. ID: {task.get('id')}")
                    print(f"     Title: {task.get('title')}")
                    print(f"     Role: {task.get('role')}")
                    print(f"     Assigned to: {task.get('assigned_to', 'Unassigned')}")
                    print(f"     Status: {task.get('status', 'Unknown')}")
                    print(f"     Sprint ID: {task.get('sprint_id')}")
                    print()
                
                return sprint_id, tasks
            else:
                print(f"❌ Error getting tasks: {tasks_response.status_code}")
                print(f"Response: {tasks_response.text}")
                return None, None
                
        else:
            print(f"❌ Error creating sprint: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
        return None, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None, None

def test_get_sprint_tasks_empty_sprint():
    """Test getting tasks for a sprint with no tasks."""
    print("\n🧪 Testing GET /sprint/{sprint_id}/tasks for empty sprint...")
    
    # Create a sprint without any tasks
    payload = {
        "developers": [
            {
                "name": "Alice Johnson",
                "role": "backend",
                "available_hours_per_day": 6
            }
        ],
        "timeline_days": 10,
        "sprint_name": "Empty Sprint Test",
        "sprint_goal": "Test empty sprint tasks API"
    }
    
    try:
        # Create sprint plan (will have no tasks since none provided)
        response = requests.post(
            "http://localhost:8080/sprint/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            sprint_id = result.get("sprint_id")
            
            print(f"✅ Empty sprint created successfully!")
            print(f"Sprint ID: {sprint_id}")
            
            # Test getting tasks for empty sprint
            tasks_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
            
            if tasks_response.status_code == 200:
                tasks_result = tasks_response.json()
                tasks = tasks_result.get("tasks", [])
                
                print(f"✅ Retrieved tasks for empty sprint successfully!")
                print(f"Number of tasks returned: {len(tasks)}")
                
                if len(tasks) == 0:
                    print("✅ Empty sprint correctly returns no tasks!")
                else:
                    print(f"❌ Empty sprint returned {len(tasks)} tasks, expected 0")
                
                return sprint_id
            else:
                print(f"❌ Error getting tasks for empty sprint: {tasks_response.status_code}")
                print(f"Response: {tasks_response.text}")
                return None
                
        else:
            print(f"❌ Error creating empty sprint: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_get_sprint_tasks_invalid_sprint():
    """Test getting tasks for a non-existent sprint."""
    print("\n🧪 Testing GET /sprint/{sprint_id}/tasks for invalid sprint...")
    
    invalid_sprint_id = "invalid-sprint-id-12345"
    
    try:
        tasks_response = requests.get(f"http://localhost:8080/sprint/{invalid_sprint_id}/tasks")
        
        if tasks_response.status_code == 200:
            tasks_result = tasks_response.json()
            tasks = tasks_result.get("tasks", [])
            
            print(f"✅ API handled invalid sprint gracefully!")
            print(f"Number of tasks returned: {len(tasks)}")
            
            if len(tasks) == 0:
                print("✅ Invalid sprint correctly returns no tasks!")
            else:
                print(f"❌ Invalid sprint returned {len(tasks)} tasks, expected 0")
                
        else:
            print(f"❌ Error getting tasks for invalid sprint: {tasks_response.status_code}")
            print(f"Response: {tasks_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_add_and_remove_tasks():
    """Test adding and removing tasks from a sprint."""
    print("\n🧪 Testing task management (add/remove tasks)...")
    
    # First create a sprint
    sprint_id, original_tasks = test_get_sprint_tasks()
    
    if not sprint_id:
        print("❌ Cannot test task management without a valid sprint")
        return
    
    print(f"\n3. Testing task management for sprint {sprint_id}...")
    
    # Test adding tasks
    print("\n   Adding tasks to sprint...")
    new_task_ids = ["task_new_1", "task_new_2"]
    
    try:
        add_response = requests.post(
            f"http://localhost:8080/sprint/{sprint_id}/tasks",
            json=new_task_ids,
            headers={"Content-Type": "application/json"}
        )
        
        if add_response.status_code == 200:
            add_result = add_response.json()
            print(f"✅ {add_result.get('message')}")
            
            # Get tasks again to verify they were added
            tasks_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
            if tasks_response.status_code == 200:
                tasks_result = tasks_response.json()
                tasks_after_add = tasks_result.get("tasks", [])
                print(f"   Tasks after adding: {len(tasks_after_add)}")
                
                # Test removing tasks
                print("\n   Removing tasks from sprint...")
                remove_response = requests.delete(
                    f"http://localhost:8080/sprint/{sprint_id}/tasks",
                    json=new_task_ids,
                    headers={"Content-Type": "application/json"}
                )
                
                if remove_response.status_code == 200:
                    remove_result = remove_response.json()
                    print(f"✅ {remove_result.get('message')}")
                    
                    # Get tasks again to verify they were removed
                    tasks_response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
                    if tasks_response.status_code == 200:
                        tasks_result = tasks_response.json()
                        tasks_after_remove = tasks_result.get("tasks", [])
                        print(f"   Tasks after removing: {len(tasks_after_remove)}")
                        
                        if len(tasks_after_remove) == len(original_tasks):
                            print("✅ Task count restored to original!")
                        else:
                            print(f"❌ Task count mismatch after remove!")
                    else:
                        print(f"❌ Error getting tasks after remove: {tasks_response.status_code}")
                else:
                    print(f"❌ Error removing tasks: {remove_response.status_code}")
            else:
                print(f"❌ Error getting tasks after add: {tasks_response.status_code}")
        else:
            print(f"❌ Error adding tasks: {add_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error in task management test: {e}")

if __name__ == "__main__":
    print("Testing Sprint Tasks API...")
    print("=" * 50)
    
    # Test 1: Get tasks for a sprint with tasks
    sprint_id, tasks = test_get_sprint_tasks()
    
    # Test 2: Get tasks for an empty sprint
    empty_sprint_id = test_get_sprint_tasks_empty_sprint()
    
    # Test 3: Get tasks for invalid sprint
    test_get_sprint_tasks_invalid_sprint()
    
    # Test 4: Test adding and removing tasks
    test_add_and_remove_tasks()
    
    print("\n" + "=" * 50)
    print("Sprint Tasks API testing completed!") 