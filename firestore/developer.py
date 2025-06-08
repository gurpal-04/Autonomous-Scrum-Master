from google.cloud import firestore
from typing import List, Optional, Dict

# Initialize Firestore client
db = firestore.Client()
COLLECTION = 'developers'

def create_developer(developer_data: dict) -> str:
    """Create a new developer document in Firestore."""
    doc_ref = db.collection(COLLECTION).document()
    doc_ref.set(developer_data)
    return doc_ref.id

def get_developer(developer_id: str) -> Optional[dict]:
    """Get a developer by ID."""
    doc_ref = db.collection(COLLECTION).document(developer_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None

def update_developer(developer_id: str, developer_data: dict) -> None:
    """Update an existing developer document."""
    doc_ref = db.collection(COLLECTION).document(developer_id)
    if not doc_ref.get().exists:
        raise ValueError(f"Developer with ID {developer_id} not found")
    doc_ref.update(developer_data)

def delete_developer(developer_id: str) -> None:
    """Delete a developer document."""
    doc_ref = db.collection(COLLECTION).document(developer_id)
    if not doc_ref.get().exists:
        raise ValueError(f"Developer with ID {developer_id} not found")
    doc_ref.delete()

def list_developers() -> List[dict]:
    """List all developers."""
    docs = db.collection(COLLECTION).stream()
    developers = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        developers.append(data)
    return developers 