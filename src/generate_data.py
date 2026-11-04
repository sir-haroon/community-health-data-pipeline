import pandas as pd
import random
from pathlib import Path
from datetime import date, timedelta

random.seed(42)

# Output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)


# Generate random dates
def random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)

    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


# 1. HEALTH FACILITIES

lgas = [
    "Bida", "Minna", "Lapai", "Kontagora", "Suleja",
    "Agaie", "Agwara", "Borgu", "Bosso", "Chanchaga",
    "Edati", "Gbako", "Gurara", "Katcha", "Lavun",
    "Magama", "Mariga", "Mashegu", "Mokwa", "Moya",
    "Paikoro", "Rafi", "Rijau", "Shiroro", "Wushishi"
]

facility_types = [
    "Primary Health Centre",
    "General Hospital",
    "Specialist Hospital",
    "Community Health Centre"
]

facilities = []

for i in range(1, 41):
    facilities.append([
        i,
        f"Community Health Facility {i:02d}",
        "Niger",
        random.choice(lgas),
        random.choice(facility_types)
    ])

facilities_df = pd.DataFrame(facilities, columns=[
    "facility_id",
    "facility_name",
    "state",
    "lga",
    "facility_type"
])

facilities_df.to_csv(
    output_dir / "facilities.csv", index=False
)


# 2. PATIENTS

patients = []

for i in range(1, 16001):

    patients.append([
        i,
        f"PAT{i:06d}",
        random.choice(["Male", "Female"]),
        random_date(1950, 2010),
        random.randint(1, 40),
        random_date(2024, 2026)
    ])

patients_df = pd.DataFrame(patients, columns=[
    "patient_id",
    "patient_code",
    "gender",
    "date_of_birth",
    "facility_id",
    "registration_date"
])

patients_df.to_csv(
    output_dir / "patients.csv", index=False
)


# 3. PATIENT VISITS

visits = []

for i in range(1, 32001):

    patient_id = random.randint(1, 16000)

    # Use the patient's registered facility
    facility_id = patients_df.loc[
        patient_id - 1, "facility_id"
    ]

    visits.append([
        i,
        patient_id,
        facility_id,
        random_date(2025, 2026),
        random.choice([
            "Outpatient",
            "Emergency",
            "Follow-up",
            "Maternal Care",
            "Immunization"
        ]),
        random.choice([
            "Fever and headache",
            "General body weakness",
            "Abdominal pain",
            "Cough and chest discomfort",
            "Routine check-up",
            "Joint pain",
            "Diarrhoea",
            "Skin irritation",
            "Difficulty breathing",
            "Body temperature elevation"
        ])
    ])

visits_df = pd.DataFrame(visits, columns=[
    "visit_id",
    "patient_id",
    "facility_id",
    "visit_date",
    "visit_type",
    "symptoms"
])

visits_df.to_csv(
    output_dir / "visits.csv", index=False
)


# 4. DIAGNOSES

diagnosis_names = [
    "Malaria",
    "Typhoid fever",
    "Upper respiratory infection",
    "Gastroenteritis",
    "Hypertension",
    "Type 2 Diabetes",
    "Pneumonia",
    "Urinary tract infection",
    "Anaemia",
    "Tuberculosis",
    "Cholera",
    "Measles",
    "Acute respiratory infection",
    "Malnutrition",
    "Skin infection"
]

diagnoses = []

for i in range(1, 32001):

    visit = visits_df.iloc[i - 1]

    diagnoses.append([
        i,
        visit["visit_id"],
        random.choice(diagnosis_names),
        f"DX{i:06d}",
        visit["visit_date"]
    ])

diagnoses_df = pd.DataFrame(diagnoses, columns=[
    "diagnosis_id",
    "visit_id",
    "diagnosis_name",
    "diagnosis_code",
    "diagnosis_date"
])

diagnoses_df.to_csv(
    output_dir / "diagnoses.csv", index=False
)


# 5. TREATMENTS

treatment_names = [
    "Artemisinin combination therapy",
    "Oral rehydration solution",
    "Paracetamol",
    "Antibiotics",
    "Antihypertensive medication",
    "Insulin therapy",
    "Antimalarial medication",
    "Iron supplements",
    "Vitamin supplementation",
    "Lifestyle counselling",
    "Antifungal medication",
    "Zinc supplementation",
    "Oral medication",
    "Clinical observation",
    "Referral for specialist care"
]

treatments = []

for i in range(1, 32001):

    visit = visits_df.iloc[i - 1]

    treatments.append([
        i,
        visit["visit_id"],
        random.choice(treatment_names),
        random.choice([
            "Once daily",
            "Twice daily",
            "Three times daily",
            "As prescribed"
        ]),
        visit["visit_date"]
    ])

treatments_df = pd.DataFrame(treatments, columns=[
    "treatment_id",
    "visit_id",
    "treatment_name",
    "dosage",
    "treatment_date"
])

treatments_df.to_csv(
    output_dir / "treatments.csv", index=False
)


# 6. GENERATE SUMMARY

print("\nCOMMUNITY HEALTH DATA GENERATION COMPLETE")
print("=" * 45)

datasets = {
    "facilities.csv": facilities_df,
    "patients.csv": patients_df,
    "visits.csv": visits_df,
    "diagnoses.csv": diagnoses_df,
    "treatments.csv": treatments_df
}

total_records = 0

for filename, dataframe in datasets.items():

    records = len(dataframe)
    total_records += records

    print(f"{filename}: {records:,} records")

print("=" * 45)
print(f"TOTAL RECORDS GENERATED: {total_records:,}")
print("\nAll datasets saved successfully!")