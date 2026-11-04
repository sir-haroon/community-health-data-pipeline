import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# Connect to PostgreSQL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# Retrieve monthly healthcare visits
query = text("""
    SELECT
        DATE_TRUNC('month', visit_date)::DATE AS month,
        COUNT(*) AS total_visits
    FROM visits
    GROUP BY month
    ORDER BY month;
""")

df = pd.read_sql(query, engine)


# Format dates for visualization
df["month"] = pd.to_datetime(df["month"])


# Create reports directory
project_root = Path(__file__).resolve().parent.parent
reports_dir = project_root / "reports" / "healthcare_trends"
reports_dir.mkdir(parents=True, exist_ok=True)


# Generate line chart
plt.figure(figsize=(14, 7))

plt.plot(
    df["month"],
    df["total_visits"],
    marker="o",
    linewidth=2
)

plt.title(
    "Monthly Healthcare Visits (2025-2026)",
    fontsize=16
)

plt.xlabel("Month", fontsize=12)
plt.ylabel("Number of Healthcare Visits", fontsize=12)

plt.xticks(rotation=45)

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()


# Save chart
output_path = reports_dir / "monthly_healthcare_visits.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()

print(f"Chart successfully saved to: {output_path}")


# Close database connection
engine.dispose()