from pydantic import BaseModel
from typing import Optional, List

class IssueBase(BaseModel):
    location: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    issue_type: str
    description: str
    urgency: str
    people_affected: int
    status: str = "open"

class IssueCreate(IssueBase):
    pass

class Issue(IssueBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class VolunteerBase(BaseModel):
    name: str
    skills: str
    availability: str
    location: str
    lat: Optional[float] = None
    lon: Optional[float] = None

class VolunteerCreate(VolunteerBase):
    pass

class Volunteer(VolunteerBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class MatchBase(BaseModel):
    issue_id: int
    volunteer_id: int
    score: float

class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
