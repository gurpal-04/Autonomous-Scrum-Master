from firestore import epic
from dotenv import load_dotenv
import os

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS: test", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
epic_data = {
    "title": "AI-Powered Task Estimator",
    "description": "An agent that estimates task complexity using LLMs.",
    "created_by": "admin"
}

# Create an epic
epic_id = epic.create_epic(epic_data)
print("✅ Created Epic ID:", epic_id)   

# Fetch the epic
fetched = epic.get_epic(epic_id)
print("📦 Fetched Epic:", fetched)

# Update the epic
epic.update_epic(epic_id, {"description": "Updated description with more detail"})
print("✏️ Updated Epic")

# List all epics
epics = epic.list_epics()
print("📋 All Epics:", epics)

# Optional: Delete the epic
# epic.delete_epic(epic_id)
# print("🗑️ Deleted Epic")
