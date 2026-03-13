# Housing-API
A RESTful API for exploring and analysing UK residential property transaction data based on the HM Land Registry Price Paid dataset. The API allows users to query property sales using flexible filters such as location, price range, property type, and date. In addition to standard property search functionality, the system provides analytical endpoints for exploring housing market trends.

The API is built using FastAPI and PostgreSQLs. Users can retrieve individual property records, perform full CRUD operations, and access analytical insights such as average price trends over time and the most expensive streets within a given area.

A lightweight frontend interface is also included to demonstrate API functionality, allowing users to search properties and visualise price trends through an interactive chart.

Key features include:
	•	Property search with filters for location, price, date, and property type
	•	Full CRUD operations for property records
	•	Analytical endpoints for price trends and high-value streets
	•	RESTful architecture with structured JSON responses
	•	PostgreSQL-backed storage for scalable querying

## API Documentation

The full API documentation is available here:

[API Documentation](API_documentation.pdf)

# Using the API
* The location field takes UK towns, cities,postcode prefixes and complete postcodes allowing alot of flexibility when searching.
* The dataset the API uses, HM Land Registry Price Paid dataset, only contains years 1995 to the Current Year.
* The property types are as follows: D - Detatched, F - Flat, S - Semi detached, T - Terraced.
* The tenure types are as follows: F - Freehold, L - Leasehold

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

If you want to create your own database follow **4. Option 1** if not, follow **4. Option 2**
# 4. Option 1 - Install PostgreSQL
1. Open database.py and choose the corresponding DATABASE_URL

  If using Mac:
2. brew install postgresql

  If using Windows: 
2.	Download installer from: https://www.postgresql.org/download/windows/
3.	Run the installer

  If using Linux:
2. sudo apt update
3. sudo apt install postgresql postgresql-contrib

Verify with psql --version

## Create the database
1. createdb housing_db
2. verify it exists with: psql -l
3. python -m scripts.create_tables
4. python -m scripts.download_and_import {start year} {end year}
  e.g python -m scripts.download_and_import 2021 2023
  This may take a few minutes and beware the greater difference between star year and end year the longer it takes to run. The HM Land Registry Price Paid dataset only contains years 1995 to the current year, so do not try to import years from before or after this period.

# 4. Option 2 - Use pre-created database implemented with render - only includes years 2021 - 2023
1. Open database.py and choose the corresponding DATABASE_URL

# 5. Run the API
1. uvicorn app.main:app --reload
2. Access the API:
* API root: http://127.0.0.1:8000/
* API frontend: http://127.0.0.1:8000/app
* Interactive documentation (Swagger UI): http://127.0.0.1:8000/docs
* OpenAPI schema: http://127.0.0.1:8000/openapi.json

## Deployed version - only includes years 2021 - 2023
* Deployed API root: https://housing-api-sofs.onrender.com
* Deployed API frontend: https://housing-api-sofs.onrender.com/app
* Deployed Interactive documentation: https://housing-api-sofs.onrender.com/docs

Please note this API was developed and tested on MacOS
