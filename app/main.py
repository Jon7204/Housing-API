from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import SessionLocal
from .models import Property

app = FastAPI()


# Proper dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Housing API running"}


@app.get("/properties/count")
def property_count(db: Session = Depends(get_db)):
    count = db.query(func.count(Property.id)).scalar()
    return {"total_properties": count}


@app.get("/properties/average-price")
def average_price(
    postcode: str = Query(...),
    db: Session = Depends(get_db)
):
    avg_price = (
        db.query(func.avg(Property.price))
        .filter(Property.postcode == postcode)
        .scalar()
    )

    if avg_price is None:
        return {"postcode": postcode, "average_price": None}

    return {
        "postcode": postcode,
        "average_price": round(avg_price, 2)
    }