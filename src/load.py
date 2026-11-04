import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Locate processed data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data", "processed")

# Load datasets in dependency order
datasets = {
    "facilities": "facilities.csv",
    "patients": "patients.csv",
    "visits": "visits.csv",
    "diagnoses": "diagnoses.csv",
    "treatments": "treatments.csv"
}

try:
    for table_name, filename in datasets.items():

        file_path = os.path.join(DATA_FOLDER, filename)

        print(f"\nLoading {filename}...")

        df = pd.read_csv(file_path)

        # Convert date columns
        for column in df.columns:
            if "date" in column.lower():
                df[column] = pd.to_datetime(df[column]).dt.date

        # Load records into PostgreSQL
        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            chunksize=1000
        )

        print(f"Successfully loaded {len(df):,} records into {table_name}")

    print("\nALL DATASETS LOADED SUCCESSFULLY!")

except Exception as error:
    print("\nDATA LOADING FAILED!")
    print(error)

finally:
    engine.dispose()