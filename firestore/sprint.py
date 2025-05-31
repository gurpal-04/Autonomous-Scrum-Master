from firestore.firestore_client import db
from datetime import datetime, timezone
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS: sprint", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

SPRINT_COLLECTION = "sprints"

# ---------- SPRINT CRUD ----------

def create_sprint(data: dict) -> str:
    data["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).add(data)
    return doc_ref[1].id

def get_sprint(sprint_id: str):
    doc = db.collection(SPRINT_COLLECTION).document(sprint_id).get()
    return doc.to_dict() | {"id": doc.id} if doc.exists else None

def update_sprint(sprint_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    db.collection(SPRINT_COLLECTION).document(sprint_id).update(updates)

def delete_sprint(sprint_id: str):
    db.collection(SPRINT_COLLECTION).document(sprint_id).delete()

def list_sprints() -> List[dict]:
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection(SPRINT_COLLECTION).stream()]

# ---------- COMMENTS ----------

def add_comment(sprint_id: str, comment: dict) -> str:
    comment["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("comments").add(comment)
    return doc_ref[1].id

def get_comments(sprint_id: str) -> List[dict]:
    comments_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("comments")
    return [doc.to_dict() | {"id": doc.id} for doc in comments_ref.stream()]

# ---------- ACTIVITY LOG ----------

def log_activity(sprint_id: str, activity: dict) -> str:
    activity["timestamp"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("activity").add(activity)
    return doc_ref[1].id

def get_activity_log(sprint_id: str) -> List[dict]:
    activity_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("activity")
    return [doc.to_dict() | {"id": doc.id} for doc in activity_ref.order_by("timestamp").stream()]
