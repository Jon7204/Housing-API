from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from fastapi.staticfiles import StaticFiles

from .schemas import PropertyBase, PropertyCreate, PropertyUpdate, PropertyResponse
from .database import SessionLocal
from .models import Property
from .utils import is_postcode, is_postcode_prefix




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
def average_price( location: str = Query(...), db: Session = Depends(get_db)):
    location = location.upper()

    if is_postcode(location):
        avg_price = (
            db.query(func.avg(Property.price))
            .filter(Property.postcode == location)
            .scalar()
        )

    elif is_postcode_prefix(location):
        avg_price = (
            db.query(func.avg(Property.price))
            .filter(Property.postcode.like(f"{location}%"))
            .scalar()
        )

    else:
        avg_price = (
            db.query(func.avg(Property.price))
            .filter(Property.town_city.ilike(f"%{location}%"))
            .scalar()
        )


    if avg_price is None:
        return {"location": location, "average_price": None}

    return {
        "location": location,
        "average_price": round(avg_price, 2)
    }



@app.get("/properties", response_model=List[PropertyBase])
def get_properties(
    location: Optional[str] = None,
    property_type: Optional[List[str]] = Query(None),
    start: Optional[date] = None,
    end: Optional[date] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort_by: Optional[str] = Query(None, description="price, -price, date, -date"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Property)

    # Filtering
    if location:
        location = location.upper()

        if is_postcode(location):
            query = query.filter(Property.postcode == location)

        elif is_postcode_prefix(location):
            query = query.filter(Property.postcode.like(f"{location}%"))

        else:
            query = query.filter(Property.town_city.ilike(f"%{location}%"))

    if property_type:
        property_type = [pt.upper() for pt in property_type]
        query = query.filter(Property.property_type.in_(property_type))

    if start:
        query = query.filter(Property.transfer_date >= start)

    if end:
        query = query.filter(Property.transfer_date <= end)
    
    if min_price and max_price:
        if max_price < min_price:
            raise HTTPException(
                status_code=400,
                detail="max_price must be greater than or equal to min_price"
            )

     # Price range
    if min_price:
        query = query.filter(Property.price >= min_price)

    if max_price:
        query = query.filter(Property.price <= max_price)

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
    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail="No properties found matching the criteria"
        )
    return results

@app.get("/properties/{property_id}", response_model=PropertyBase)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property_obj = (
        db.query(Property)
        .filter(Property.id == property_id)
        .first()
    )

    if property_obj is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property_obj

@app.post("/properties", response_model=PropertyResponse, status_code=201)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    new_property = Property(**property_data.model_dump())

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property

@app.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(Property.id == property_id).first()

    if property_obj is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for key, value in property_data.model_dump().items():
        setattr(property_obj, key, value)

    db.commit()
    db.refresh(property_obj)

    return property_obj

@app.delete("/properties/{property_id}", status_code=204)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter(Property.id == property_id).first()

    if property_obj is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(property_obj)
    db.commit()

    return

from sqlalchemy import func

@app.get("/analytics/price-trend")
def price_trend(
    location: Optional[str] = None,
    property_type: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(
        func.extract("year", Property.transfer_date).label("year"),
        func.avg(Property.price).label("avg_price")
    )

    if location:
        query = query.filter(Property.town_city.ilike(f"%{location}%"))

    if property_type:
        property_type = [pt.upper() for pt in property_type]
        query = query.filter(Property.property_type.in_(property_type))

    results = (
        query.group_by("year")
        .order_by("year")
        .all()
    )

    return [
        {"year": int(r.year), "average_price": round(r.avg_price, 2)}
        for r in results
    ]

app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")