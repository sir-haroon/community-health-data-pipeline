import os
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Data directory
DATA_DIR = Path("data/raw")

# Define loading order
datasets = {
    "facilities": "facilities.csv",
    "patients": "patients.csv",
    "visits": "visits.csv",
    "diagnoses": "diagnoses.csv",
    "treatments": "treatments.csv"
}

# Convert date columns to proper date objects
date_columns = {
    "patients": ["date_of_birth", "registration_date"],
    "visits": ["visit_date"],
    "diagnoses": ["diagnosis_date"],
    "treatments": ["treatment_date"]
}


try:
    with engine.begin() as connection:

        # Prevent accidental duplicate loading
        for table in datasets:

            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar()

            if count > 0:
                raise ValueError(
                    f"The {table} table is not empty. "
                    "Loading cancelled to prevent duplicates."
                )

        print("\nSTARTING DATA LOADING")
        print("=" * 45)

        total_records = 0

        for table, filename in datasets.items():

            print(f"\nLoading {filename}...")

            # Read CSV
            df = pd.read_csv(DATA_DIR / filename)

            # Convert date columns
            if table in date_columns:
                for column in date_columns[table]:
                    df[column] = pd.to_datetime(
                        df[column]
                    ).dt.date

            # Load into PostgreSQL
            df.to_sql(
                name=table,
                con=connection,
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi"
            )

            records = len(df)
            total_records += records

            print(f"Successfully loaded {records:,} records.")

        # Update PostgreSQL ID sequences
        id_columns = {
            "facilities": "facility_id",
            "patients": "patient_id",
            "visits": "visit_id",
            "diagnoses": "diagnosis_id",
            "treatments": "treatment_id"
        }

        for table, column in id_columns.items():

            connection.execute(
                text(f"""
                    SELECT setval(
                        pg_get_serial_sequence(
                            'public.{table}', '{column}'
                        ),
                        (SELECT MAX({column}) FROM {table}),
                        true
                    )
                """)
            )

        print("\nDATA LOADING COMPLETED!")
        print("=" * 45)
        print(f"Total records loaded: {total_records:,}")

except Exception as error:

    print("\nDATA LOADING FAILED!")
    print(error)

finally:
    engine.dispose()