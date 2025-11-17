"""
Test file demonstrating the simplified Sprint Planning API usage.

The sprint planner agent now expects structured data with tasks and developers.
Planning results are stored as task IDs in the sprint document.
"""

import requests
import json
import time

# Example API call for sprint planning
def test_sprint_planning():
    """Test the sprint planning endpoint with the new data structure."""
    
    # Example payload with tasks and developers
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
        "sprint_name": "Authentication Sprint",
        "sprint_goal": "Complete user authentication feature with login/logout functionality"
    }
    
    # Make API call (assuming server is running on localhost:8080)
    try:
        response = requests.post(
            "http://localhost:8080/sprint/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sprint planning successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Test retrieving the stored tasks
            if "sprint_id" in result:
                test_sprint_task_management(result["sprint_id"])
                
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_sprint_planning_with_firestore_data():
    """
    Test sprint planning without providing tasks/developers.
    The API will fetch data from Firestore automatically.
    """
    
    # Minimal payload - API will fetch tasks and developers from Firestore
    payload = {
        "timeline_days": 14,
        "sprint_name": "Firestore Data Sprint",
        "sprint_goal": "Plan sprint using existing tasks and developers from database"
    }
    
    try:
        response = requests.post(
            "http://localhost:8080/sprint/plan", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sprint planning with Firestore data successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Test retrieving the stored tasks
            if "sprint_id" in result:
                test_sprint_task_management(result["sprint_id"])
                
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_sprint_task_management(sprint_id: str):
    """Test sprint task management functionality."""
    print(f"\n🔧 Testing task management for sprint {sprint_id}...")
    
    try:
        # Get tasks in the sprint
        response = requests.get(f"http://localhost:8080/sprint/{sprint_id}/tasks")
        
        if response.status_code == 200:
            tasks_data = response.json()
            print("✅ Retrieved sprint tasks successfully!")
            print(f"Number of tasks: {len(tasks_data.get('tasks', []))}")
            
            # Test adding tasks to sprint
            test_add_tasks_to_sprint(sprint_id)
            
            # Test removing tasks from sprint
            test_remove_tasks_from_sprint(sprint_id)
            
            # Test updating task assignments
            test_update_task_assignments(sprint_id)
            
            return tasks_data
        else:
            print(f"❌ Error retrieving sprint tasks: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing task management: {e}")

def test_add_tasks_to_sprint(sprint_id: str):
    """Test adding tasks to a sprint."""
    print(f"\n➕ Testing adding tasks to sprint {sprint_id}...")
    
    # This would typically be done with existing task IDs
    # For testing, we'll use dummy task IDs
    dummy_task_ids = ["task1", "task2"]
    
    try:
        response = requests.post(
            f"http://localhost:8080/sprint/{sprint_id}/tasks",
            json=dummy_task_ids,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Added tasks to sprint successfully!")
            print(f"Result: {result}")
        else:
            print(f"❌ Error adding tasks: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing add tasks: {e}")

def test_remove_tasks_from_sprint(sprint_id: str):
    """Test removing tasks from a sprint."""
    print(f"\n➖ Testing removing tasks from sprint {sprint_id}...")
    
    # Remove the dummy tasks we added
    dummy_task_ids = ["task1", "task2"]
    
    try:
        response = requests.delete(
            f"http://localhost:8080/sprint/{sprint_id}/tasks",
            json=dummy_task_ids,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Removed tasks from sprint successfully!")
            print(f"Result: {result}")
        else:
            print(f"❌ Error removing tasks: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing remove tasks: {e}")

def test_update_task_assignments(sprint_id: str):
    """Test updating task assignments."""
    print(f"\n👥 Testing task assignments for sprint {sprint_id}...")
    
    # Example assignments
    assignments = {
        "task1": "Alice Johnson",
        "task2": "Bob Smith"
    }
    
    try:
        response = requests.post(
            f"http://localhost:8080/sprint/{sprint_id}/assignments",
            json=assignments,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Updated task assignments successfully!")
            print(f"Result: {result}")
        else:
            print(f"❌ Error updating assignments: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing task assignments: {e}")

def test_sprint_details(sprint_id: str):
    """Test retrieving the sprint details."""
    print(f"\n📋 Testing retrieval of sprint details for sprint {sprint_id}...")
    
    try:
        response = requests.get(f"http://localhost:8080/sprint/{sprint_id}")
        
        if response.status_code == 200:
            sprint_data = response.json()
            print("✅ Retrieved sprint details successfully!")
            print(f"Sprint name: {sprint_data.get('name')}")
            print(f"Sprint goal: {sprint_data.get('goal')}")
            print(f"Status: {sprint_data.get('status')}")
            print(f"Team size: {sprint_data.get('team_size')}")
            print(f"Total tasks: {sprint_data.get('total_tasks')}")
            print(f"Planned tasks: {sprint_data.get('planned_tasks_count')}")
            print(f"Unassigned tasks: {sprint_data.get('unassigned_tasks_count')}")
            print(f"Planned task IDs: {sprint_data.get('planned_task_ids', [])}")
            
            return sprint_data
        else:
            print(f"❌ Error retrieving sprint details: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing sprint details retrieval: {e}")

def test_duplicate_task_titles():
    """Test sprint planning with tasks that have the same title but different descriptions."""
    print(f"\n🔄 Testing duplicate task titles scenario...")
    
    # Example payload with tasks that have the same title but different descriptions
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
                "title": "Implement user authentication",
                "description": "Add OAuth2 integration for social login",
                "role": "backend",
                "estimate_hours": 12,
                "sprint_points": 5
            },
            {
                "title": "Design login page UI",
                "description": "Create responsive login form with validation",
                "role": "frontend", 
                "estimate_hours": 12,
                "sprint_points": 5
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
            }
        ],
        "timeline_days": 10,
        "sprint_name": "Duplicate Titles Test Sprint",
        "sprint_goal": "Test handling of tasks with duplicate titles"
    }
    
    try:
        response = requests.post(
            "http://localhost:8080/sprint/plan",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sprint planning with duplicate titles successful!")
            print(f"Sprint ID: {result.get('sprint_id')}")
            print(f"Planned task IDs: {result.get('planned_task_ids', [])}")
            print(f"Number of planned task IDs: {len(result.get('planned_task_ids', []))}")
            print(f"Number of planned tasks: {len(result.get('planned_tasks', []))}")
            
            # Verify that all planned tasks have corresponding IDs
            if len(result.get('planned_task_ids', [])) == len(result.get('planned_tasks', [])):
                print("✅ All planned tasks have corresponding IDs!")
            else:
                print("❌ Mismatch between planned tasks and task IDs!")
                print(f"Expected {len(result.get('planned_tasks', []))} task IDs, got {len(result.get('planned_task_ids', []))}")
            
            # Test retrieving the stored tasks
            if "sprint_id" in result:
                test_sprint_task_management(result["sprint_id"])
                
            return result
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8080")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("Testing Simplified Sprint Planning API with Task Management...")
    
    print("\n1. Testing with provided tasks and developers:")
    result1 = test_sprint_planning()
    
    if result1 and "sprint_id" in result1:
        test_sprint_details(result1["sprint_id"])
    
    print("\n" + "="*50)
    
    print("\n2. Testing with Firestore data:")
    result2 = test_sprint_planning_with_firestore_data()
    
    if result2 and "sprint_id" in result2:
        test_sprint_details(result2["sprint_id"])
    
    print("\n" + "="*50)
    
    print("\n3. Testing duplicate task titles:")
    result3 = test_duplicate_task_titles() 