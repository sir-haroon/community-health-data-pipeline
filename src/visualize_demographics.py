import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables

load_dotenv()

# PostgreSQL connection

DATABASE_URL = (
f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
f"{os.getenv('DB_PASSWORD')}@"
f"{os.getenv('DB_HOST')}:"
f"{os.getenv('DB_PORT')}/"
f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

print("Successfully connected to PostgreSQL!")

# Create reports directory

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports" / "demographics"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================

# 1. AGE DISTRIBUTION

# ==========================================

age_query = """
SELECT
CASE
WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) < 18
THEN 'Under 18'
WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) BETWEEN 18 AND 29
THEN '18-29'
WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) BETWEEN 30 AND 44
THEN '30-44'
WHEN EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) BETWEEN 45 AND 59
THEN '45-59'
ELSE '60+'
END AS age_group,
COUNT(*) AS total_patients
FROM patients
GROUP BY age_group
ORDER BY MIN(EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)));
"""

age_df = pd.read_sql_query(age_query, engine)

print("\nAGE DISTRIBUTION")
print(age_df)

plt.figure(figsize=(10, 6))
plt.bar(age_df["age_group"], age_df["total_patients"])
plt.title("Patient Age Distribution")
plt.xlabel("Age Group")
plt.ylabel("Number of Patients")
plt.tight_layout()

plt.savefig(REPORTS_DIR / "age_distribution.png", dpi=300)
plt.close()

print("Age distribution saved successfully!")

# ==========================================

# 2. GENDER DISTRIBUTION

# ==========================================

gender_query = """
SELECT
gender,
COUNT(*) AS total_patients
FROM patients
GROUP BY gender
ORDER BY total_patients DESC;
"""

gender_df = pd.read_sql_query(gender_query, engine)

print("\nGENDER DISTRIBUTION")
print(gender_df)

plt.figure(figsize=(8, 6))

plt.pie(
gender_df["total_patients"],
labels=gender_df["gender"],
autopct="%1.1f%%",
startangle=90
)

plt.title("Patient Gender Distribution")
plt.tight_layout()

plt.savefig(REPORTS_DIR / "gender_distribution.png", dpi=300)
plt.close()

print("Gender distribution saved successfully!")

# ==========================================

# 3. PATIENT DISTRIBUTION BY LGA

# ==========================================

location_query = """
SELECT
f.lga,
COUNT(p.patient_id) AS total_patients
FROM patients p
JOIN facilities f
ON p.facility_id = f.facility_id
GROUP BY f.lga
ORDER BY total_patients DESC
LIMIT 10;
"""

location_df = pd.read_sql_query(location_query, engine)

print("\nPATIENT DISTRIBUTION BY LGA")
print(location_df)

plt.figure(figsize=(12, 7))

plt.barh(
location_df["lga"],
location_df["total_patients"]
)

plt.title("Top 10 LGAs by Patient Population")
plt.xlabel("Number of Patients")
plt.ylabel("Local Government Area")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(REPORTS_DIR / "patient_distribution_by_lga.png", dpi=300)
