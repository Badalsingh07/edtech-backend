from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class AssignmentCreate(BaseModel):
    title: str
    description: str
    teacher_id: int

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    class Config:
        from_attributes = True

class SubmissionCreate(BaseModel):
    student_id: int
    file_url: str

class SubmissionOut(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    file_url: str
    class Config:
        from_attributes = True

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    created_by: int
    class Config:
        from_attributes = True