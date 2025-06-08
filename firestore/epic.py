from dotenv import load_dotenv
import os

from firestore.firestore_client import get_collection_ref, db

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALSepic:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

EPIC_COLLECTION = "epics"

def save_epic(epic_id: str, data: dict):
    ref = get_collection_ref(EPIC_COLLECTION)
    ref.document(epic_id).set(data)

def get_epic(epic_id: str):
    ref = get_collection_ref(EPIC_COLLECTION)
    return ref.document(epic_id).get().to_dict()

def list_epics():
    ref = get_collection_ref(EPIC_COLLECTION)
    epics = []
    all_story_ids = set()  # Track unique story IDs across all epics
    epic_docs = []  # Store epic docs temporarily
    
    # First pass: collect all epic data and story IDs
    for doc in ref.stream():
        epic_data = doc.to_dict()
        epic_data["id"] = doc.id
        story_ids = epic_data.get("stories", [])
        if story_ids:
            all_story_ids.update(story_ids)
        epic_docs.append(epic_data)
    
    # Batch get all stories in one operation
    stories_dict = {}
    if all_story_ids:
        stories_ref = get_collection_ref("stories")
        # Convert to list because get() expects a sequence
        story_refs = [stories_ref.document(sid) for sid in all_story_ids]
        # Get all stories in a single batch operation
        story_snapshots = db.get_all(story_refs)
        
        # Create a lookup dictionary
        for snap in story_snapshots:
            if snap.exists:
                story_data = snap.to_dict()
                stories_dict[snap.id] = {
                    "id": snap.id,
                    "title": story_data.get("title", "Untitled Story")
                }
    
    # Second pass: attach story data to epics
    for epic_data in epic_docs:
        story_ids = epic_data.get("stories", [])
        epic_data["stories"] = [
            stories_dict[sid]
            for sid in story_ids
            if sid in stories_dict
        ]
        epics.append(epic_data)
    
    return epics

def create_epic(data: dict) -> str:
    """Creates a new epic document and returns its ID"""
    ref = get_collection_ref(EPIC_COLLECTION)
    doc_ref = ref.document()  # Creates a document with auto-generated ID
    doc_ref.set(data)
    return doc_ref.id

def update_epic(epic_id: str, data: dict):
    """Updates an existing epic document with the provided data"""
    ref = get_collection_ref(EPIC_COLLECTION)
    doc_ref = ref.document(epic_id)
    doc_ref.update(data)

def delete_epic(epic_id: str):
    """Deletes an epic document"""
    ref = get_collection_ref(EPIC_COLLECTION)
    doc_ref = ref.document(epic_id)
    doc_ref.delete()
