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

tables = [
    "facilities",
    "patients",
    "visits",
    "diagnoses",
    "treatments"
]

total_records = 0

try:
    with engine.connect() as connection:

        print("\nDATABASE VERIFICATION")
        print("=" * 40)

        for table in tables:

            query = text(f"SELECT COUNT(*) FROM {table}")

            count = connection.execute(query).scalar()

            total_records += count

            print(f"{table.capitalize():15} {count:,} records")

        print("=" * 40)
        print(f"TOTAL RECORDS: {total_records:,}")

        if total_records == 112040:
            print("\nDATABASE VERIFICATION SUCCESSFUL!")

except Exception as error:
    print("Verification failed:")
    print(error)

finally:
    engine.dispose()