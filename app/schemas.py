from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


class PropertyBase(BaseModel):
    id: int
    price: int
    transfer_date: date
    postcode: Optional[str] = None
    property_type: Optional[str] = None
    tenure: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)