from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# If using local PostgreSQL, the URL would be:
#DATABASE_URL = "postgresql://localhost/housing_db"
# If using external PostgreSQL, the URL would be:
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()