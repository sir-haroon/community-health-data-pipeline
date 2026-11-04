import os
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

print("Successfully connected to PostgreSQL!")

# Retrieve the 10 most common diagnoses
query = """
SELECT
    diagnosis_name,
    COUNT(*) AS total_cases
FROM diagnoses
GROUP BY diagnosis_name
ORDER BY total_cases DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)

# Close database connection
conn.close()

# Display results
print("\nTOP 10 MOST COMMON DIAGNOSES")
print(df)

# Create reports directory if it doesn't exist
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports" / "healthcare_trends"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Create visualization
plt.figure(figsize=(12, 7))

plt.barh(
    df["diagnosis_name"],
    df["total_cases"]
)

plt.xlabel("Number of Cases")
plt.ylabel("Diagnosis")
plt.title("Top 10 Most Common Diagnoses")

plt.gca().invert_yaxis()

plt.tight_layout()

# Save visualization
plt.savefig(
    REPORTS_DIR / "top_10_diagnoses.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nVisualization successfully saved!")
print(f"Location: {REPORTS_DIR / 'top_10_diagnoses.png'}")