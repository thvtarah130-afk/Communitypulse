from .database_firestore import db as firestore_db
from . import schemas
from typing import List, Optional

# Collections
ISSUES_COL = "issues"
VOLUNTEERS_COL = "volunteers"
MATCHES_COL = "matches"

def create_issue(db, issue: schemas.IssueCreate):
    issue_dict = issue.dict()
    doc_ref = firestore_db.collection(ISSUES_COL).document()
    issue_dict["id"] = doc_ref.id
    doc_ref.set(issue_dict)
    return issue_dict

def get_issues(db, limit: int = 100):
    docs = firestore_db.collection(ISSUES_COL).limit(limit).stream()
    issues = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        issues.append(data)
    return issues

def create_volunteer(db, volunteer: schemas.VolunteerCreate):
    vol_dict = volunteer.dict()
    doc_ref = firestore_db.collection(VOLUNTEERS_COL).document()
    vol_dict["id"] = doc_ref.id
    doc_ref.set(vol_dict)
    return vol_dict

def get_volunteers(db, limit: int = 100):
    docs = firestore_db.collection(VOLUNTEERS_COL).limit(limit).stream()
    vols = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        vols.append(data)
    return vols

def create_match(db, match: schemas.MatchBase):
    match_dict = match.dict()
    doc_ref = firestore_db.collection(MATCHES_COL).document()
    match_dict["id"] = doc_ref.id
    doc_ref.set(match_dict)
    return match_dict

def get_matches(db):
    docs = firestore_db.collection(MATCHES_COL).stream()
    matches = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        matches.append(data)
    return matches

def clear_matches(db):
    docs = firestore_db.collection(MATCHES_COL).list_documents()
    for doc in docs:
        doc.delete()
