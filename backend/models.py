from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    issue_type = Column(String, index=True)
    description = Column(Text)
    urgency = Column(String)  # low, medium, high
    people_affected = Column(Integer)
    status = Column(String, default="open")  # open, matched, closed

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skills = Column(String)  # Comma-separated list of skills
    availability = Column(String)
    location = Column(String)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, index=True)
    volunteer_id = Column(Integer, index=True)
    score = Column(Float)
