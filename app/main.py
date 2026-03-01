from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import SessionLocal
from .models import Property

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Housing API is running"}


@app.get("/properties/count")
def property_count(db: Session = next(get_db())):
    count = db.query(func.count(Property.id)).scalar()
    return {"total_properties": count}