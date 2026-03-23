from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int
    course: str

class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True