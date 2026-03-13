from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# If using local PostgreSQL, the URL would be:
#DATABASE_URL = "postgresql://localhost/housing_db"
# If using external PostgreSQL, the URL would be:
DATABASE_URL = "postgresql://housing_db_k5j7_user:nUNlRanASFI1aQFnAR6PKEWFoAv1t6HM@dpg-d6q2d0aa214c73f8vsdg-a/housing_db_k5j7"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()