import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load database credentials
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

try:

    with engine.connect() as connection:

        # QUERY 7: Patient distribution by facility
        print("\nPATIENT DISTRIBUTION BY FACILITY")
        print("=" * 70)

        facility_query = text("""
            SELECT
                f.facility_name,
                f.lga,
                COUNT(p.patient_id) AS total_patients
            FROM facilities f
            LEFT JOIN patients p
                ON f.facility_id = p.facility_id
            GROUP BY
                f.facility_id,
                f.facility_name,
                f.lga
            ORDER BY total_patients DESC;
        """)

        facility_results = pd.read_sql(
            facility_query, connection
        )

        print(facility_results.to_string(index=False))

        # QUERY 9: Most frequently recorded diagnoses
        print("\n\nMOST FREQUENTLY RECORDED DIAGNOSES")
        print("=" * 70)

        diagnosis_query = text("""
            SELECT
                diagnosis_name,
                COUNT(*) AS total_cases
            FROM diagnoses
            GROUP BY diagnosis_name
            ORDER BY total_cases DESC;
        """)

        diagnosis_results = pd.read_sql(
            diagnosis_query, connection
        )

        print(diagnosis_results.to_string(index=False))

        print("\n\nANALYSIS COMPLETED SUCCESSFULLY!")

except Exception as error:

    print("Error retrieving results:")
    print(error)

finally:
    engine.dispose()