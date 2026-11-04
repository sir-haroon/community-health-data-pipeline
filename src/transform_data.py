import pandas as pd
from pathlib import Path

# Define directories
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("\nSTARTING DATA TRANSFORMATION")
print("=" * 50)

# Load datasets
facilities = pd.read_csv(RAW_DIR / "facilities.csv")
patients = pd.read_csv(RAW_DIR / "patients.csv")
visits = pd.read_csv(RAW_DIR / "visits.csv")
diagnoses = pd.read_csv(RAW_DIR / "diagnoses.csv")
treatments = pd.read_csv(RAW_DIR / "treatments.csv")


# 1. Standardise text fields
text_datasets = [
    facilities,
    patients,
    visits,
    diagnoses,
    treatments
]

for df in text_datasets:

    for column in df.select_dtypes(include="str").columns:

        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )


# 2. Remove duplicate records
facilities = facilities.drop_duplicates(
    subset=["facility_id"]
)

patients = patients.drop_duplicates(
    subset=["patient_id"]
)

visits = visits.drop_duplicates(
    subset=["visit_id"]
)

diagnoses = diagnoses.drop_duplicates(
    subset=["diagnosis_id"]
)

treatments = treatments.drop_duplicates(
    subset=["treatment_id"]
)


# 3. Convert date columns
date_columns = {
    "patients": (patients, [
        "date_of_birth", "registration_date"
    ]),
    "visits": (visits, ["visit_date"]),
    "diagnoses": (diagnoses, ["diagnosis_date"]),
    "treatments": (treatments, ["treatment_date"])
}

for name, (df, columns) in date_columns.items():

    for column in columns:

        df[column] = pd.to_datetime(
            df[column], errors="coerce"
        )


# 4. Validate patient registration dates
invalid_dates = patients[
    patients["date_of_birth"] > patients["registration_date"]
]

print(
    f"Patients with invalid birth dates: {len(invalid_dates)}"
)


# 5. Correct visits before registration
patient_dates = patients[
    ["patient_id", "registration_date"]
]

visits = visits.merge(
    patient_dates,
    on="patient_id",
    how="left"
)

invalid_visits = visits[
    visits["visit_date"] < visits["registration_date"]
]

print(
    f"Visits before patient registration: {len(invalid_visits)}"
)

visits["visit_date"] = visits[
    ["visit_date", "registration_date"]
].max(axis=1)

visits = visits.drop(
    columns=["registration_date"]
)


# 6. Synchronise diagnosis and treatment dates
visit_dates = visits[
    ["visit_id", "visit_date"]
]

diagnoses = diagnoses.drop(
    columns=["diagnosis_date"]
).merge(
    visit_dates,
    on="visit_id",
    how="left"
)

diagnoses = diagnoses.rename(
    columns={"visit_date": "diagnosis_date"}
)

treatments = treatments.drop(
    columns=["treatment_date"]
).merge(
    visit_dates,
    on="visit_id",
    how="left"
)

treatments = treatments.rename(
    columns={"visit_date": "treatment_date"}
)


# 7. Format dates for CSV output
for df, columns in [
    (patients, ["date_of_birth", "registration_date"]),
    (visits, ["visit_date"]),
    (diagnoses, ["diagnosis_date"]),
    (treatments, ["treatment_date"])
]:

    for column in columns:

        df[column] = df[column].dt.strftime("%Y-%m-%d")


# 8. Save processed datasets
datasets = {
    "facilities.csv": facilities,
    "patients.csv": patients,
    "visits.csv": visits,
    "diagnoses.csv": diagnoses,
    "treatments.csv": treatments
}

print("\nSAVING PROCESSED DATA")
print("=" * 50)

for filename, df in datasets.items():

    df.to_csv(
        PROCESSED_DIR / filename,
        index=False
    )

    print(f"{filename}: {len(df):,} records")


print("\nDATA TRANSFORMATION COMPLETED!")
print("=" * 50)