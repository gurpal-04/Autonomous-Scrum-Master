from firestore.firestore_client import db
from datetime import datetime, timezone
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS: story", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

STORY_COLLECTION = "stories"
# ---------- STORY CRUD ----------

def create_story(data: dict) -> str:
    data["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(STORY_COLLECTION).add(data)
    return doc_ref[1].id

def get_story(story_id: str):
    doc = db.collection(STORY_COLLECTION).document(story_id).get()
    return doc.to_dict() | {"id": doc.id} if doc.exists else None

def update_story(story_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    db.collection(STORY_COLLECTION).document(story_id).update(updates)

def delete_story(story_id: str):
    db.collection(STORY_COLLECTION).document(story_id).delete()

def list_stories() -> List[dict]:
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection(STORY_COLLECTION).stream()]

# ---------- COMMENTS ----------

def add_comment(story_id: str, comment: dict) -> str:
    comment["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(STORY_COLLECTION).document(story_id).collection("comments").add(comment)
    return doc_ref[1].id

def get_comments(story_id: str) -> List[dict]:
    comments_ref = db.collection(STORY_COLLECTION).document(story_id).collection("comments")
    return [doc.to_dict() | {"id": doc.id} for doc in comments_ref.stream()]

# ---------- ACTIVITY LOG ----------

def log_activity(story_id: str, activity: dict) -> str:
    activity["timestamp"] = datetime.now(timezone.utc)
    doc_ref = db.collection(STORY_COLLECTION).document(story_id).collection("activity").add(activity)
    return doc_ref[1].id

def get_activity_log(story_id: str) -> List[dict]:
    activity_ref = db.collection(STORY_COLLECTION).document(story_id).collection("activity")
    return [doc.to_dict() | {"id": doc.id} for doc in activity_ref.order_by("timestamp").stream()]
