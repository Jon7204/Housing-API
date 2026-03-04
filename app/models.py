from sqlalchemy import Column, Integer, String, Date, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False)
    transfer_date = Column(Date, nullable=False)
    postcode = Column(String, nullable=False)
    property_type = Column(String)
    tenure = Column(String)

    __table_args__ = (
        Index("idx_postcode", "postcode"),
        Index("idx_transfer_date", "transfer_date"),
        Index("idx_postcode_transfer_date", "postcode", "transfer_date"),
    )