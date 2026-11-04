import pandas as pd
import os

DATA_FOLDER = "data/processed"

files = [
    "facilities.csv",
    "patients.csv",
    "visits.csv",
    "diagnoses.csv",
    "treatments.csv"
]

for file in files:
    path = os.path.join(DATA_FOLDER, file)

    print("\n" + "=" * 60)
    print(f"DATASET: {file}")
    print("=" * 60)

    if not os.path.exists(path):
        print(f"FILE NOT FOUND: {path}")
        continue

    df = pd.read_csv(path)

    print("\nDATA TYPES:")
    print(df.dtypes)

    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    print("\nFIRST TWO RECORDS:")
    print(df.head(2))

    print("\nTOTAL RECORDS:")
    print(len(df))