from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False)
    transfer_date = Column(Date, nullable=False)
    postcode = Column(String(10), index=True)
    property_type = Column(String(5))
    tenure = Column(String(20))