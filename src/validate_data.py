import pandas as pd
from pathlib import Path

data_dir = Path("data/raw")

# Load datasets
facilities = pd.read_csv(data_dir / "facilities.csv")
patients = pd.read_csv(data_dir / "patients.csv")
visits = pd.read_csv(data_dir / "visits.csv")
diagnoses = pd.read_csv(data_dir / "diagnoses.csv")
treatments = pd.read_csv(data_dir / "treatments.csv")

datasets = {
    "Facilities": facilities,
    "Patients": patients,
    "Visits": visits,
    "Diagnoses": diagnoses,
    "Treatments": treatments
}

print("\nDATA QUALITY REPORT")
print("=" * 50)

# 1. Record counts
for name, df in datasets.items():
    print(f"{name}: {len(df):,} records")

# 2. Missing values
print("\nMISSING VALUES")
for name, df in datasets.items():
    missing = df.isnull().sum().sum()
    print(f"{name}: {missing}")

# 3. Duplicate IDs
print("\nDUPLICATE IDENTIFIERS")

id_columns = {
    "Facilities": (facilities, "facility_id"),
    "Patients": (patients, "patient_id"),
    "Visits": (visits, "visit_id"),
    "Diagnoses": (diagnoses, "diagnosis_id"),
    "Treatments": (treatments, "treatment_id")
}

for name, (df, column) in id_columns.items():
    duplicates = df[column].duplicated().sum()
    print(f"{name}: {duplicates}")

# 4. Foreign key validation
print("\nFOREIGN KEY VALIDATION")

print(
    "Patients with invalid facilities:",
    (~patients["facility_id"].isin(
        facilities["facility_id"]
    )).sum()
)

print(
    "Visits with invalid patients:",
    (~visits["patient_id"].isin(
        patients["patient_id"]
    )).sum()
)

print(
    "Visits with invalid facilities:",
    (~visits["facility_id"].isin(
        facilities["facility_id"]
    )).sum()
)

print(
    "Diagnoses with invalid visits:",
    (~diagnoses["visit_id"].isin(
        visits["visit_id"]
    )).sum()
)

print(
    "Treatments with invalid visits:",
    (~treatments["visit_id"].isin(
        visits["visit_id"]
    )).sum()
)

print("\nVALIDATION COMPLETE")