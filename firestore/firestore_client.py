from google.cloud import firestore
from dotenv import load_dotenv
import os

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALScc:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
db = firestore.Client()

def get_collection_ref(name: str):
    return db.collection(name)
