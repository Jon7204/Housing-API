import sys
import requests
import pandas as pd
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Property

MIN_YEAR = 1995
MAX_YEAR = 2025   # update occasionally if needed



BASE_URL = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-{}.csv"


def import_year(year: int, db: Session):

    url = BASE_URL.format(year)
    print(f"Downloading {year}...")

    response = requests.get(url, stream=True)
    response.raise_for_status()

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

        print(f"{year}: inserted {len(records)} rows")


def main():

    if len(sys.argv) != 3:
        print("Usage: python -m scripts.download_and_import <start_year> <end_year>")
        sys.exit(1)

    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    if start_year < MIN_YEAR or end_year > MAX_YEAR:
        print(f"Valid year range is {MIN_YEAR}-{MAX_YEAR}")
        sys.exit(1)

    if start_year > end_year:
        print("start_year must be less than or equal to end_year")
        sys.exit(1)

    db: Session = SessionLocal()

    for year in range(start_year, end_year + 1):
        try:
            import_year(year, db)
        except Exception as e:
            print(f"Failed to import {year}: {e}")

    db.close()
    print("Import finished.")


if __name__ == "__main__":
    main()