from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# If following 4. Option 1 use:
#DATABASE_URL = "postgresql://localhost/housing_db"

# If following 4. Option 2 use:
#DATABASE_URL = "postgresql://housing_db_k5j7_user:nUNlRanASFI1aQFnAR6PKEWFoAv1t6HM@dpg-d6q2d0aa214c73f8vsdg-a.frankfurt-postgres.render.com/housing_db_k5j7"

# URL for External server to host:
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()