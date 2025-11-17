#!/usr/bin/env python3
"""
Example usage of the chat agent with function tools.
This script demonstrates how the agent handles various user queries.
"""

import json
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# Configuration
APP_NAME = "scrum_assistant"
USER_ID = "user123"
SESSION_ID = "session123"

def run_conversation():
    """Run a conversation with the chat agent."""
    
    # Set up session and runner
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    
    # Example conversation
    conversations = [
        "Hello! I'm new to this Scrum system.",
        "Create a task called 'Fix login bug' with high priority",
        "The login form is not working properly on mobile devices",
        "List all tasks",
        "Create a developer profile for John Doe with email john.doe@example.com and skills Python, JavaScript, React",
        "List all developers",
        "Assign John Doe to the login bug task",
        "Show me tasks assigned to John Doe",
        "Create an epic for User Authentication System with critical priority",
        "Update the login bug task status to in_progress"
    ]
    
    print("🤖 AI Scrum Assistant Demo")
    print("=" * 50)
    
    for i, user_message in enumerate(conversations, 1):
        print(f"\n👤 User {i}: {user_message}")
        print("-" * 30)
        
        # Create content for the message
        content = types.Content(role='user', parts=[types.Part(text=user_message)])
        
        # Run the agent
        events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
        
        # Process events
        for event in events:
            if event.is_final_response():
                response = event.content.parts[0].text
                print(f"🤖 Assistant: {response}")
                break
        
        print()

def main():
    """Main function to run the example."""
    print("Starting AI Scrum Assistant conversation demo...")
    print("Note: Make sure your API server is running on http://localhost:8080")
    print()
    
    try:
        run_conversation()
        print("\n✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Make sure your API server is running and accessible.")

if __name__ == "__main__":
    main() 