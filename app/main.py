from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date

from .schemas import PropertyBase
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



@app.get("/properties", response_model=List[PropertyBase])
def get_properties(
    postcode: Optional[str] = None,
    property_type: Optional[str] = None,
    start: Optional[date] = None,
    end: Optional[date] = None,
    sort_by: Optional[str] = Query(None, description="price, -price, date, -date"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Property)

    # Filtering
    if postcode:
        query = query.filter(Property.postcode == postcode)

    if property_type:
        query = query.filter(Property.property_type == property_type)

    if start:
        query = query.filter(Property.transfer_date >= start)

    if end:
        query = query.filter(Property.transfer_date <= end)

    # Sorting
    if sort_by:
        if sort_by == "price":
            query = query.order_by(Property.price)
        elif sort_by == "-price":
            query = query.order_by(Property.price.desc())
        elif sort_by == "date":
            query = query.order_by(Property.transfer_date)
        elif sort_by == "-date":
            query = query.order_by(Property.transfer_date.desc())
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid sort_by value. Use: price, -price, date, -date"
            )

    results = query.limit(limit).offset(offset).all()

    return results