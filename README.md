# Housing-API
A backend system that stores housing data and answers questions about rent and affordability.

# Using the API
* The location field takes UK towns, cities,postcode prefixes and complete postcodes allowing alot of flexibility when searching.
* The dataset the API uses, HM Land Registry Price Paid dataset, only contains years 1995 to the Current Year.
* The property types are as follows: D - Detatched, F - Flat, S - Semi detached, T - Terraced.
* The tenure types are as follows: F - Freehold, L - Leasehold

## API Documentation

The full API documentation is available here:

[API Documentation](API_documentation.pdf)

# To run the API:

# 1. Clone Repository
1. git clone https://github.com/Jon7204/Housing-API.git
2. Ensure pwd is the root of the repo

# 2. Setup Virtual Environment
1. python -m venv venv

  If using Mac/Linux:

2. source venv/bin/activate

  If using Windows:

2. venv\Scripts\activate

# 3. Install Dependencies
1. pip install -r requirements.txt

# 4. Install PostgreSQL
  If using Mac:
1. brew install postgresql

  If using Windows: 
1.	Download installer from: https://www.postgresql.org/download/windows/
2.	Run the installer

  If using Linux:
1. sudo apt update
2. sudo apt install postgresql postgresql-contrib

Verify with psql --version

# 5. Create the database
1. createdb housing_db
2. verify it exists with: psql -l
3. python -m scripts.create_tables
4. python -m scripts.download_and_import {start year} {end year}
  e.g python -m scripts.download_and_import 2021 2023
  This may take a few minutes and beware the greater difference between star year and end year the longer it takes to run. The HM Land Registry Price Paid dataset only contains years 1995 to the current year, so do not try to import years from before or after this period.

# 6. Run the API
1. uvicorn app.main:app --reload
2. Access the API:
* API root: http://127.0.0.1:8000/
* API frontend: http://127.0.0.1:8000/app
* Interactive documentation (Swagger UI): http://127.0.0.1:8000/docs
* OpenAPI schema: http://127.0.0.1:8000/openapi.json
