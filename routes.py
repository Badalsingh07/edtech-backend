from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from passlib.hash import bcrypt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserOut)
def signup(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):
    user_in_db = db.query(models.User).filter(models.User.username == username).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = bcrypt.hash(password)
    new_user = models.User(username=username, password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    user_in_db = db.query(models.User).filter(models.User.username == user.username).first()
    if not user_in_db or not bcrypt.verify(user.password, user_in_db.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return { "message": "Login successful", "user_id": user_in_db.id, "role": user_in_db.role }

@router.post("/assignments", response_model=schemas.AssignmentOut)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    new_assignment = models.Assignment(
        title=assignment.title,
        description=assignment.description,
        created_by=assignment.teacher_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.post("/assignments/{assignment_id}/submit", response_model=schemas.SubmissionOut)
def submit_assignment(assignment_id: int, submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    new_submission = models.Submission(
        assignment_id=assignment_id,
        student_id=submission.student_id,
        file_url=submission.file_url
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

@router.get("/assignments/{assignment_id}/submissions", response_model=list[schemas.SubmissionOut])
def view_submissions(assignment_id: int, db: Session = Depends(get_db)):
    submissions = db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
    return submissions
@router.get("/assignments", response_model=list[schemas.AssignmentOut])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()