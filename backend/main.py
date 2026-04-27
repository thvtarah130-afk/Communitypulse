from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
import pandas as pd
from typing import List, Optional
import io
import os
from pydantic import BaseModel

from . import models, schemas, crud, matching, nlp_engine
from .database import engine, get_db

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Community Insight & Volunteer Matching System")

@app.get("/")
async def root():
    return {"message": "Community Insight API is running"}

# 1. POST /upload-data
@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            # Fallback for text data or other formats if needed
            # For now, we assume CSV as requested
            raise HTTPException(status_code=400, detail="Only CSV files are supported for now.")
        
        count = 0
        for _, row in df.iterrows():
            # Clean and normalize
            description = str(row.get("description", "")).strip()
            if not description:
                continue
                
            issue_type = row.get("issue_type", "auto")
            if issue_type == "auto" or pd.isna(issue_type):
                issue_type = nlp_engine.categorize_issue(description)
            
            issue = schemas.IssueCreate(
                location=str(row.get("location", "Unknown")),
                lat=float(row.get("lat", 0.0)) if pd.notna(row.get("lat")) else None,
                lon=float(row.get("lon", 0.0)) if pd.notna(row.get("lon")) else None,
                issue_type=issue_type,
                description=description,
                urgency=str(row.get("urgency", "medium")).lower(),
                people_affected=int(row.get("people_affected", 1)) if pd.notna(row.get("people_affected")) else 1,
            )
            crud.create_issue(db, issue)
            count += 1
        return {"message": f"Successfully processed and uploaded {count} community records."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

# 2. POST /add-volunteer
@app.post("/add-volunteer", response_model=schemas.Volunteer)
def add_volunteer(volunteer: schemas.VolunteerCreate, db: Session = Depends(get_db)):
    return crud.create_volunteer(db=db, volunteer=volunteer)

# 3. GET /needs (Analyzed and Ranked)
@app.get("/needs", response_model=List[schemas.Issue])
def get_needs(db: Session = Depends(get_db)):
    issues = crud.get_issues(db)
    
    # Ranking logic: Urgency (High=3, Med=2, Low=1) * log(People Affected)
    # Plus frequency of issue type in the same location (simplified)
    def rank_score(issue):
        urgency_map = {"high": 3, "medium": 2, "low": 1}
        u_score = urgency_map.get(issue.urgency.lower(), 1)
        p_score = issue.people_affected
        return u_score * (p_score ** 0.5) # Square root to dampen large numbers

    sorted_issues = sorted(issues, key=rank_score, reverse=True)
    return sorted_issues

# 4. GET /volunteers
@app.get("/volunteers", response_model=List[schemas.Volunteer])
def list_volunteers(db: Session = Depends(get_db)):
    return crud.get_volunteers(db)

# 5. GET /match (Return matches, trigger calculation if needed)
@app.get("/match")
def get_matches(db: Session = Depends(get_db)):
    issues = crud.get_issues(db)
    volunteers = crud.get_volunteers(db)
    
    # Trigger matching algorithm
    new_matches = matching.match_volunteers_to_issues(issues, volunteers)
    
    # We don't necessarily persist all matches in this GET call for simplicity, 
    # but we return the top matches calculated.
    return new_matches

# Optional: Add manual entry for needs via POST (matching frontend form)
@app.post("/add-need", response_model=schemas.Issue)
def add_need(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    if not issue.issue_type or issue.issue_type.lower() == "auto":
        issue.issue_type = nlp_engine.categorize_issue(issue.description)
    return crud.create_issue(db=db, issue=issue)
