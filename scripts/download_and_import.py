import requests
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Property


DATA_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2023.csv"


def import_data_streaming():
    print("Streaming housing data...")

    response = requests.get(DATA_URL, stream=True)
    response.raise_for_status()

    db: Session = SessionLocal()

    # Tell pandas to read from raw HTTP stream
    chunk_iter = pd.read_csv(
        response.raw,
        header=None,
        chunksize=5000
    )

    for chunk in chunk_iter:
        chunk = chunk.dropna(subset=[1, 2])

        records = []

        for _, row in chunk.iterrows():
            records.append({
                "price": int(row[1]),
                "transfer_date": row[2],
                "postcode": row[3],
                "property_type": row[4],
                "tenure": row[6],
                "paon": row[7],
                "street": row[9],
                "town_city": row[11]
            })

        db.bulk_insert_mappings(Property, records)
        db.commit()
        print(f"Committed {len(records)} rows")

 

    db.close()
    print("Import complete.")


if __name__ == "__main__":
    import_data_streaming()