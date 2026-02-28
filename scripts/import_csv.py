import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Property


def import_csv(file_path):
    df = pd.read_csv(file_path, nrows=10000)  # limit rows

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        try:
            property_obj = Property(
                price=int(row["price"]),
                transfer_date=datetime.strptime(
                    row["date_of_transfer"], "%Y-%m-%d"
                ),
                postcode=row["postcode"],
                property_type=row["property_type"],
                tenure=row["tenure"]
            )
            db.add(property_obj)

        except Exception:
            continue

    db.commit()
    db.close()

    print("Data imported successfully.")


if __name__ == "__main__":
    import_csv("data/housing.csv")