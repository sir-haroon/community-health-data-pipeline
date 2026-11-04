import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

queries = {

    "Total Patients": """
        SELECT COUNT(*) AS total_patients
        FROM patients;
    """,

    "Total Healthcare Visits": """
        SELECT COUNT(*) AS total_visits
        FROM visits;
    """,

    "Most Common Diagnoses": """
        SELECT diagnosis_name, COUNT(*) AS diagnosis_count
        FROM diagnoses
        GROUP BY diagnosis_name
        ORDER BY diagnosis_count DESC
        LIMIT 10;
    """,

    "Visits by Facility": """
        SELECT f.facility_name, COUNT(v.visit_id) AS total_visits
        FROM facilities f
        JOIN visits v ON f.facility_id = v.facility_id
        GROUP BY f.facility_name
        ORDER BY total_visits DESC
        LIMIT 10;
    """,

    "Visits by Type": """
        SELECT visit_type, COUNT(*) AS total_visits
        FROM visits
        GROUP BY visit_type
        ORDER BY total_visits DESC;
    """,

     "Monthly Healthcare Visits": """
        SELECT
        DATE_TRUNC('month', visit_date)::DATE AS month,
        COUNT(*) AS total_visits
        FROM visits
        GROUP BY month
        ORDER BY month;
    """,
}

try:

    with engine.connect() as connection:

        for title, query in queries.items():

            print("\n" + "=" * 60)
            print(title.upper())
            print("=" * 60)

            result = connection.execute(text(query))

            for row in result:
                print(row)

except Exception as error:
    print("Analytics failed:")
    print(error)

finally:
    engine.dispose()