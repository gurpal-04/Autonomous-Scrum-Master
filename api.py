import os
import json
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
# from custom_routes import router as custom_router
from routes import epic, user_story, sprint, task_routes, developer_routes
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Handle Google credentials
def setup_google_credentials():
    try:
        # First check for JSON file (local development)
        if os.path.exists("demo1112-07e56190d678.json"):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "demo1112-07e56190d678.json"
            logger.info("Using local credentials file")
            return
            
        # If no file, try environment variable (Render or .env file)
        creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if creds_json:
            # For local development, the JSON might be a string representation
            if isinstance(creds_json, str) and creds_json.startswith('{'):
                creds_json = json.loads(creds_json)
            
            # Create a temporary file to store credentials
            creds_path = "/tmp/google-credentials.json" if os.getenv('RENDER') else "temp-credentials.json"
            with open(creds_path, 'w') as f:
                if isinstance(creds_json, dict):
                    json.dump(creds_json, f)
                else:
                    f.write(creds_json)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
            logger.info("Successfully set up Google credentials from environment")
        else:
            logger.warning("No Google credentials found in file or environment variables")
    except Exception as e:
        logger.error(f"Error setting up Google credentials: {e}")

# Set up credentials before anything else
setup_google_credentials()

# Set up paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR  # Parent directory containing multi_tool_agent

# Set up DB path for sessions
SESSION_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sessions.db')}"

# Create the FastAPI app using ADK's helper
app: FastAPI = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url=SESSION_DB_URL,
    allow_origins=["*"],  # In production, restrict this
    web=False,  # Enable the ADK Web UI
)

# app.include_router(custom_router)
app.include_router(epic.router)
app.include_router(user_story.router)
app.include_router(sprint.router)
app.include_router(task_routes.router)
app.include_router(developer_routes.router)

# Add custom endpoints
@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"message": "test"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

# Add a test middleware to log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Request query params: {request.query_params}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

if __name__ == "__main__":
    # Use the PORT environment variable, defaulting to 8080
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)