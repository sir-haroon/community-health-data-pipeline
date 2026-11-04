import pandas as pd
from pathlib import Path

# Locate processed data
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FOLDER = BASE_DIR / "data" / "processed"

# Load datasets
facilities = pd.read_csv(DATA_FOLDER / "facilities.csv")
patients = pd.read_csv(DATA_FOLDER / "patients.csv")
visits = pd.read_csv(DATA_FOLDER / "visits.csv")
diagnoses = pd.read_csv(DATA_FOLDER / "diagnoses.csv")
treatments = pd.read_csv(DATA_FOLDER / "treatments.csv")


def check_duplicates(df, column, dataset):
    duplicates = df[column].duplicated().sum()

    print(f"{dataset} duplicate {column}: {duplicates}")


def check_foreign_keys(child, column, parent, parent_column, relationship):
    invalid = (~child[column].isin(parent[parent_column])).sum()

    print(f"{relationship}: {invalid} invalid references")


print("\n" + "=" * 60)
print("DATABASE RELATIONSHIP VALIDATION")
print("=" * 60)

# Check primary keys
check_duplicates(facilities, "facility_id", "Facilities")
check_duplicates(patients, "patient_id", "Patients")
check_duplicates(visits, "visit_id", "Visits")
check_duplicates(diagnoses, "diagnosis_id", "Diagnoses")
check_duplicates(treatments, "treatment_id", "Treatments")

print("\nFOREIGN KEY VALIDATION")

# Patients
check_foreign_keys(
    patients, "facility_id",
    facilities, "facility_id",
    "Patients -> Facilities"
)

# Visits
check_foreign_keys(
    visits, "patient_id",
    patients, "patient_id",
    "Visits -> Patients"
)

check_foreign_keys(
    visits, "facility_id",
    facilities, "facility_id",
    "Visits -> Facilities"
)

# Diagnoses
check_foreign_keys(
    diagnoses, "visit_id",
    visits, "visit_id",
    "Diagnoses -> Visits"
)

# Treatments
check_foreign_keys(
    treatments, "visit_id",
    visits, "visit_id",
    "Treatments -> Visits"
)

print("\nVALIDATION COMPLETED")
print("=" * 60)