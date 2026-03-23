from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home_screen():
    return {"message": "Welcome to Home Screen"}


@app.get("/students")
def get_students(name: str = None, course: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Student)

    if name:
        query = query.filter(models.Student.name.contains(name))  

    if course:
        query = query.filter(models.Student.course == course)

    return query.all()


# POST
@app.post("/students", status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.model_dump()) 
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# GET by ID
@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# PUT
@app.put("/students/{id}")
def update_student(id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in updated.model_dump().items(): 
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


# DELETE
@app.delete("/students/{id}", status_code=204)
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()