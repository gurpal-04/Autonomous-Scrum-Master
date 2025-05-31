from dotenv import load_dotenv
import os

from firestore.firestore_client import get_collection_ref
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
    return [doc.to_dict() for doc in ref.stream()]

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
