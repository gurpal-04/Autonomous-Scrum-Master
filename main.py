from fastapi import FastAPI
from google.adk.core.runtime import AgentRuntime
from google.adk.core.api.api_server import register_adk_routes
from custom_routes import router as custom_router  # your custom endpoints

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR
SESSION_DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'sessions.db')}"

# Create FastAPI app
app = FastAPI()

# Initialize ADK agent runtime
runtime = AgentRuntime(
    agent_dir=AGENT_DIR,
    session_db_url=SESSION_DB_URL,
)

# Register ADK's internal endpoints into our app
register_adk_routes(app, runtime)

# Register custom endpoints
app.include_router(custom_router)

# Optional: Add logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
