import os
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

# Create database connection
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# Read SQL schema
with open("sql/schema.sql", "r") as file:
    schema = file.read()

# Execute SQL statements
try:
    with engine.begin() as connection:
        connection.execute(text(schema))

    print("Successfully created all database tables!")

except Exception as error:
    print("Table creation failed:")
    print(error)