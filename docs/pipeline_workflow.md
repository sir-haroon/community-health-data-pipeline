# Community Health Data Pipeline Workflow

## Overview

This project demonstrates an end-to-end data pipeline for organising, transforming, validating, storing, and analysing community healthcare data.

The pipeline uses Python, Pandas, PostgreSQL, SQL, and Matplotlib.

## Pipeline Architecture

The workflow follows these stages:

1. Data generation and extraction
2. Data inspection
3. Data transformation and cleaning
4. Data validation
5. Database creation and loading
6. SQL analysis
7. Data visualisation

## 1. Data Generation and Extraction

The project includes scripts for generating and extracting healthcare datasets.

Main scripts:

* `src/generate_data.py`
* `src/extract.py`

The datasets cover:

* Healthcare facilities
* Patients
* Healthcare visits
* Diagnoses
* Treatments

Raw datasets are stored in `data/raw/`.

## 2. Data Inspection

Initial data inspection helps identify structural issues, missing values, inconsistent formats, and potential data quality problems.

Main script:

`src/inspect_data.py`

## 3. Data Transformation

The transformation stage prepares the datasets for analysis and database storage.

Activities include data cleaning, formatting, and preparation of structured datasets.

Main scripts:

* `src/transform.py`
* `src/transform_data.py`

Transformed datasets are stored in `data/processed/`.

## 4. Data Validation

Validation scripts help assess data quality and consistency before and after database loading.

Main scripts:

* `src/validate_data.py`
* `src/validate_relationships.py`

Relationship validation checks for duplicate identifiers and invalid foreign key references.

## 5. Database Creation and Loading

PostgreSQL provides the relational database used to store the healthcare datasets.

Main scripts:

* `src/create_tables.py`
* `src/load.py`
* `src/load_data.py`

The database schema is defined in `sql/schema.sql`.

## 6. SQL Analysis

SQL queries are used to retrieve and analyse information from the database.

The analysis includes:

* Total healthcare facilities
* Total registered patients
* Total healthcare visits
* Total diagnoses
* Total treatments
* Patient distribution by gender
* Patient distribution by facility and LGA
* Visits by visit type
* Most frequent diagnoses
* Most frequent treatments

SQL queries are maintained in `sql/analysis.sql`.

## 7. Data Analysis and Visualisation

Python and Matplotlib are used to generate visual reports.

The project includes:

### Demographic Analysis

* Age distribution
* Gender distribution
* Patient distribution by LGA

Output directory:

`reports/demographics/`

### Healthcare Trend Analysis

* Monthly healthcare visits
* Top 10 diagnoses

Output directory:

`reports/healthcare_trends/`

Main visualisation scripts:

* `src/visualize_demographics.py`
* `src/visualize_data.py`
* `src/visualize_diagnoses.py`

Additional analytical scripts include:

* `src/analytics.py`
* `src/advanced_analysis.py`

## 8. Database Verification

The database verification process checks the loaded database records.

Main scripts:

* `src/verify_database.py`
* `src/query_results.py`

## Project Directory Structure

```text
community-health-data-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── database_schema.md
│   └── pipeline_workflow.md
│
├── logs/
│
├── reports/
│   ├── demographics/
│   └── healthcare_trends/
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
└── src/
    ├── generate_data.py
    ├── extract.py
    ├── inspect_data.py
    ├── transform.py
    ├── transform_data.py
    ├── validate_data.py
    ├── validate_relationships.py
    ├── create_tables.py
    ├── load.py
    ├── load_data.py
    ├── analytics.py
    ├── advanced_analysis.py
    ├── query_results.py
    ├── verify_database.py
    ├── visualize_data.py
    ├── visualize_demographics.py
    └── visualize_diagnoses.py
```

## Technologies

* Python
* Pandas
* PostgreSQL
* SQL
* Matplotlib
* SQLAlchemy
* Psycopg2
* Python-dotenv
