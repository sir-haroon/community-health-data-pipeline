import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

try:

    with engine.connect() as connection:

        print("\nMONTHLY HEALTHCARE VISIT ANALYSIS")
        print("=" * 75)

        query = text("""
            WITH monthly_visits AS (

                SELECT
                    DATE_TRUNC('month', visit_date) AS month,
                    COUNT(*) AS total_visits

                FROM visits

                GROUP BY DATE_TRUNC('month', visit_date)
            )

            SELECT
                TO_CHAR(month, 'Mon YYYY') AS month,
                total_visits,

                LAG(total_visits) OVER (
                    ORDER BY month
                ) AS previous_month_visits,

                ROUND(
                    (
                        (total_visits -
                        LAG(total_visits) OVER (
                            ORDER BY month
                        ))::NUMERIC
                        /
                        NULLIF(
                            LAG(total_visits) OVER (
                                ORDER BY month
                            ), 0
                        )
                    ) * 100,
                    2
                ) AS percentage_change

            FROM monthly_visits

            ORDER BY month;
        """)

        results = pd.read_sql(query, connection)

        print(results.to_string(index=False))

        print("\nMONTHLY ANALYSIS COMPLETED!")

except Exception as error:

    print("Analysis failed:")
    print(error)

finally:
    engine.dispose()