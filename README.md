# US Sales Tax Rates
This is a simple script that loads a directory of CSV files into a MySQL database

# Requirements
 * MySQL server accessible by your app
 * Python 3

# Setup (env variables)
```bash
# environment variables passed into app
export TAX_RATES_DB_HOST=localhost
export TAX_RATES_DB_PORT=3306
export TAX_RATES_DB_NAME=tax_rates
export TAX_RATES_DB_USER=user_tax
export TAX_RATES_DB_PASS=unclesam

export FLASK_APP=app.py
```

# Install (manual)
 * `git clone git@github.com:mikesparr/us-sales-tax-rates.git`
 * `cd us-sales-tax-rates`
 * `python3 -m venv /path/to/env`
 * `source /path/to/env/bin/activate`
 * `pip install -r requirements.txt`
 * `source .env` (where you set up env var)

## Loading data from CSV into database
 * `python loader.py`

## Running application and exposing API
 * `python app.py`

# Install (Docker)
Using Docker Compose, this can spin up a database and app container that can 
see each other. Note that the `mysql` image wasn't working loading data, so I 
switched to `mariadb` image and it works. The pause for users to load may not 
be necessary in the `run` script but added just in case.

`docker-compose up`

# Usage
http://localhost:5000/rate/94123  (where 94123 is a 5-digit US zip code)

`curl localhost:5000/rate/94123`

Returns:
```javascript
{
  "error": null,
  "rate": {
    "estimated_city_rate": 0.0,
    "estimated_combined_rate": 0.085,
    "estimated_county_rate": 0.0025,
    "risk_level": 2.0,
    "state_code": "CA",
    "state_rate": 0.06,
    "tax_region": "SAN FRANCISCO COUNTY",
    "zip_code": 94123
  }
}
```

# Database Access
`mysql --host=127.0.0.1 --port=32000 -u root -p`

