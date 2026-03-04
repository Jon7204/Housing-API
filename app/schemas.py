from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


# Base shared fields
class PropertyBase(BaseModel):
    id: int
    price: int
    transfer_date: date
    postcode: Optional[str] = None
    property_type: Optional[str] = None
    tenure: Optional[str] = None


# Schema used when creating a property
class PropertyCreate(PropertyBase):
    pass


# Schema used when updating a property
class PropertyUpdate(PropertyBase):
    pass


# Schema returned from API (includes ID)
class PropertyResponse(PropertyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)