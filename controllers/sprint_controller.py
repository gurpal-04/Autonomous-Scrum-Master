from fastapi import HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.sprint_planner import root_agent as sprint_planner_agent
from agents.sprint_planner.agent import PlanningInput, AssignedTask, Developer
from google.genai import types
from dotenv import load_dotenv
from firestore import sprint
from firestore import developer as developer_module
from firestore import task as task_module
from typing import Dict, Any, List
import json
from datetime import datetime, timezone

load_dotenv()

# Initialize the session service once
session_service = InMemorySessionService()
USER_ID = "gurpalsingh"
APP_NAME = "sprint planner"


async def plan_sprint_logic(payload: Dict[str, Any]):
    """
    Plan a sprint by providing structured data to the sprint planner agent.
    
    Expected payload format:
    {
        "tasks": [
            {
                "title": "Task title",
                "description": "Task description", 
                "role": "frontend",
                "estimate_hours": 8,
                "sprint_points": 5
            }
        ],
        "developers": [
            {
                "name": "John Doe",
                "role": "frontend",
                "available_hours_per_day": 6
            }
        ],
        "timeline_days": 10,
        "sprint_name": "Sprint 1",
        "sprint_goal": "Complete authentication feature"
    }
    """
    
    try:
        # Extract data from payload
        tasks_data = payload.get("tasks", [])
        developers_data = payload.get("developers", [])
        timeline_days = payload.get("timeline_days")
        sprint_name = payload.get("sprint_name", "Planned Sprint")
        sprint_goal = payload.get("sprint_goal", "Sprint planning completed")
        
        # If no tasks/developers provided, try to fetch from Firestore
        if not tasks_data:
            # Fetch available tasks from Firestore
            firestore_tasks = task_module.list_tasks()
            tasks_data = [
                {
                    "title": task.get("title", ""),
                    "description": task.get("description", ""),
                    "role": task.get("role", "fullstack"),
                    "estimate_hours": task.get("estimate_hours", 8),
                    "sprint_points": task.get("story_points", 5)
                }
                for task in firestore_tasks
                if not task.get("assigned_to")  # Only unassigned tasks
            ]
            
        if not developers_data:
            # Fetch available developers from Firestore
            firestore_developers = developer_module.list_developers()
            developers_data = [
                {
                    "name": dev.get("name", ""),
                    "role": dev.get("role", "fullstack"),
                    "available_hours_per_day": dev.get("available_hours_per_day", 6)
                }
                for dev in firestore_developers
            ]
        
        # Create PlanningInput object
        planning_input = PlanningInput(
            tasks=[
                AssignedTask(
                    title=task["title"],
                    description=task["description"],
                    role=task["role"],
                    estimate_hours=task["estimate_hours"],
                    sprint_points=task["sprint_points"],
                    assigned_to=None,
                    status="unassigned",
                    planned_start_day=None,
                    planned_end_day=None
                )
                for task in tasks_data
            ],
            developers=[
                Developer(
                    name=dev["name"],
                    role=dev["role"],
                    available_hours_per_day=dev["available_hours_per_day"]
                )
                for dev in developers_data
            ],
            timeline_days=timeline_days
        )
        
        # Convert to JSON string for the agent
        input_text = planning_input.model_dump_json()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing payload: {str(e)}")

    # Create a new session
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={"initial_key": "initial_value"}
    )
    SESSION_ID = new_session.id

    # Initialize the runner with the existing session service
    runner = Runner(
        agent=sprint_planner_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Prepare the user content
    user_content = types.Content(role="user", parts=[types.Part(text=input_text)])

    final_response_text = None

    try:
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_content):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during agent run: {e}")

    if final_response_text:
        try:
            # Parse the agent response to extract planned tasks
            agent_response_data = json.loads(final_response_text)
            planned_tasks = agent_response_data.get("planned_tasks", [])
            
            # Create a sprint record
            sprint_data = {
                "name": sprint_name,
                "goal": sprint_goal,
                "start_date": datetime.now(timezone.utc),
                "end_date": datetime.now(timezone.utc),  # Will be updated based on timeline
                "status": "planned",
                "capacity": sum(dev.get("available_hours_per_day", 0) for dev in developers_data),
                "timeline_days": timeline_days,
                "team_size": len(developers_data),
                "total_tasks": len(planned_tasks),
                "planned_tasks_count": len([t for t in planned_tasks if t.get("status") == "scheduled"]),
                "unassigned_tasks_count": len([t for t in planned_tasks if t.get("status") == "unassigned"]),
                "planned_task_ids": []  # Will be populated with actual task IDs
            }
            
            sprint_id = sprint.create_sprint(sprint_data)
            
            # Extract task IDs and assignments from planned tasks
            task_assignments = {}
            planned_task_ids = []
            
            print(f"Processing {len(planned_tasks)} planned tasks...")
            
            for i, task in enumerate(planned_tasks):
                # Find the corresponding task in Firestore or create a new one
                task_title = task.get("title", "")
                task_description = task.get("description", "")
                
                print(f"Processing task {i+1}: {task_title}")
                
                # Try to find existing task by title AND description for better matching
                existing_tasks = task_module.list_tasks()
                existing_task = None
                
                # Debug: Show all tasks with the same title
                tasks_with_same_title = task_module.get_tasks_by_title(task_title)
                if tasks_with_same_title:
                    print(f"  Found {len(tasks_with_same_title)} existing tasks with title '{task_title}':")
                    for t in tasks_with_same_title:
                        print(f"    - ID: {t.get('id')}, Description: {t.get('description', 'N/A')[:50]}..., Assigned: {t.get('assigned_to', 'None')}, Sprint: {t.get('sprint_id', 'None')}")
                
                # First try to find exact match by title and description
                for existing in existing_tasks:
                    if (existing.get("title") == task_title and 
                        existing.get("description") == task_description):
                        existing_task = existing
                        print(f"  Found exact match: {existing.get('id')}")
                        break
                
                # If no exact match, try to find by title only (but be more careful)
                if not existing_task:
                    # Only match by title if the task is unassigned and not already in a sprint
                    for existing in existing_tasks:
                        if (existing.get("title") == task_title and 
                            not existing.get("assigned_to") and 
                            not existing.get("sprint_id")):
                            existing_task = existing
                            print(f"  Found title match (unassigned): {existing.get('id')}")
                            break
                
                if existing_task:
                    task_id = existing_task["id"]
                    planned_task_ids.append(task_id)
                    print(f"  Using existing task: {task_id}")
                else:
                    # Create new task if no suitable match found
                    new_task_data = {
                        "title": task_title,
                        "description": task_description,
                        "role": task.get("role", "fullstack"),
                        "estimate_hours": task.get("estimate_hours", 8),
                        "story_points": task.get("sprint_points", 5),
                        "status": task.get("status", ""),
                        "sprint_id": sprint_id
                    }
                    task_id = task_module.create_task(new_task_data)
                    planned_task_ids.append(task_id)
                    print(f"  Created new task: {task_id}")
                
                # Store assignment if task is scheduled
                if task.get("status") == "scheduled" and task.get("assigned_to"):
                    task_assignments[task_id] = task.get("assigned_to")
                    print(f"  Assigned to: {task.get('assigned_to')}")
            
            print(f"Final planned_task_ids: {planned_task_ids}")
            print(f"Final task_assignments: {task_assignments}")
            
            # Add task IDs to sprint
            if planned_task_ids:
                sprint.add_tasks_to_sprint(sprint_id, planned_task_ids)
            
            # Update task assignments
            if task_assignments:
                sprint.update_task_assignments(sprint_id, task_assignments)
            
            # Log the planning activity
            sprint.log_activity(sprint_id, {
                "action": "sprint_planned",
                "description": f"Sprint planning completed with {len(planned_tasks)} tasks",
                "user": USER_ID,
                "planned_task_ids": planned_task_ids
            })
            
            return {
                "sprint_id": sprint_id,
                "planned_tasks": planned_tasks,
                "planned_task_ids": planned_task_ids,
                "task_assignments": task_assignments,
                "summary": {
                    "total_tasks": len(planned_tasks),
                    "scheduled_tasks": len([t for t in planned_tasks if t.get("status") == "scheduled"]),
                    "unassigned_tasks": len([t for t in planned_tasks if t.get("status") == "unassigned"]),
                    "team_size": len(developers_data),
                    "timeline_days": timeline_days
                }
            }
            
        except json.JSONDecodeError:
            # If agent response is not valid JSON, create sprint with basic info
            sprint_data = {
                "name": sprint_name,
                "goal": sprint_goal,
                "start_date": datetime.now(timezone.utc),
                "end_date": datetime.now(timezone.utc),
                "status": "planned",
                "planned_task_ids": []
            }
            
            sprint_id = sprint.create_sprint(sprint_data)
            
            return {
                "sprint_id": sprint_id,
                "note": "Agent response was not in expected JSON format",
                "agent_response": final_response_text
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error storing planning results: {str(e)}")
    else:
        raise HTTPException(status_code=500, detail="No response received from agent.")

async def create_sprint_logic(sprint_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        sprint_id = sprint.create_sprint(sprint_data)
        return {"id": sprint_id, "message": "Sprint created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_logic(sprint_id: str) -> Dict[str, Any]:
    try:
        result = sprint.get_sprint(sprint_id)
        if not result:
            raise HTTPException(status_code=404, detail="Sprint not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_sprint_logic(sprint_id: str, updates: Dict[str, Any]) -> Dict[str, str]:
    try:
        sprint.update_sprint(sprint_id, updates)
        return {"message": "Sprint updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_sprint_logic(sprint_id: str) -> Dict[str, str]:
    try:
        sprint.delete_sprint(sprint_id)
        return {"message": "Sprint deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_sprints_logic() -> Dict[str, List[Dict[str, Any]]]:
    try:
        sprints = sprint.list_sprints()
        return {"sprints": sprints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_sprint_comment_logic(sprint_id: str, comment: Dict[str, Any]) -> Dict[str, Any]:
    try:
        comment_id = sprint.add_comment(sprint_id, comment)
        return {"id": comment_id, "message": "Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_comments_logic(sprint_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        comments = sprint.get_comments(sprint_id)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def log_sprint_activity_logic(sprint_id: str, activity: Dict[str, Any]) -> Dict[str, Any]:
    try:
        activity_id = sprint.log_activity(sprint_id, activity)
        return {"id": activity_id, "message": "Activity logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_activity_log_logic(sprint_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        activity_log = sprint.get_activity_log(sprint_id)
        return {"activity_log": activity_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_tasks_logic(sprint_id: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get all tasks planned for a sprint."""
    try:
        tasks = sprint.get_sprint_tasks(sprint_id)
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
