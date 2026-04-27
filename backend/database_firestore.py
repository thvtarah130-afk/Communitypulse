import os
from google.cloud import firestore
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

def get_firestore_client():
    """
    Returns a Firestore client. 
    In a Cloud Run environment, this will use the service account automatically.
    Locally, it may require GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    if PROJECT_ID:
        return firestore.Client(project=PROJECT_ID)
    else:
        # Fallback to default detection
        return firestore.Client()

db = get_firestore_client()
