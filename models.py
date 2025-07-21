from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # teacher or student

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    file_url = Column(String)