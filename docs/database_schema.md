# Database Schema Documentation

## Overview

The Community Health Data Pipeline uses a relational PostgreSQL database to organise community healthcare information.

The database consists of five interconnected tables:

1. Facilities
2. Patients
3. Visits
4. Diagnoses
5. Treatments

The relationships between these tables allow healthcare data to be analysed across facilities, patients, visits, diagnoses, and treatments.

## Database Tables

### 1. Facilities

Stores information about healthcare facilities.

| Column        | Data type          | Description                         |
| ------------- | ------------------ | ----------------------------------- |
| facility_id   | SERIAL PRIMARY KEY | Unique facility identifier          |
| facility_name | VARCHAR(150)       | Name of the healthcare facility     |
| state         | VARCHAR(100)       | State where the facility is located |
| lga           | VARCHAR(100)       | Local Government Area               |
| facility_type | VARCHAR(50)        | Type of healthcare facility         |
| created_at    | TIMESTAMP          | Record creation timestamp           |

### 2. Patients

Stores patient demographic and registration information.

| Column            | Data type          | Description                       |
| ----------------- | ------------------ | --------------------------------- |
| patient_id        | SERIAL PRIMARY KEY | Unique patient identifier         |
| patient_code      | VARCHAR(50) UNIQUE | Unique patient reference code     |
| gender            | VARCHAR(20)        | Patient gender                    |
| date_of_birth     | DATE               | Patient date of birth             |
| facility_id       | INTEGER            | Reference to the facilities table |
| registration_date | DATE               | Patient registration date         |

### 3. Visits

Records healthcare visits made by patients.

| Column      | Data type          | Description                       |
| ----------- | ------------------ | --------------------------------- |
| visit_id    | SERIAL PRIMARY KEY | Unique visit identifier           |
| patient_id  | INTEGER            | Reference to the patients table   |
| facility_id | INTEGER            | Reference to the facilities table |
| visit_date  | DATE               | Date of healthcare visit          |
| visit_type  | VARCHAR(50)        | Type of visit                     |
| symptoms    | TEXT               | Reported symptoms                 |
| created_at  | TIMESTAMP          | Record creation timestamp         |

### 4. Diagnoses

Stores diagnoses recorded during healthcare visits.

| Column         | Data type          | Description                   |
| -------------- | ------------------ | ----------------------------- |
| diagnosis_id   | SERIAL PRIMARY KEY | Unique diagnosis identifier   |
| visit_id       | INTEGER            | Reference to the visits table |
| diagnosis_name | VARCHAR(150)       | Name of diagnosis             |
| diagnosis_code | VARCHAR(50)        | Diagnosis classification code |
| diagnosis_date | DATE               | Date diagnosis was recorded   |

### 5. Treatments

Stores treatments administered or prescribed during healthcare visits.

| Column         | Data type          | Description                   |
| -------------- | ------------------ | ----------------------------- |
| treatment_id   | SERIAL PRIMARY KEY | Unique treatment identifier   |
| visit_id       | INTEGER            | Reference to the visits table |
| treatment_name | VARCHAR(150)       | Name of treatment             |
| dosage         | VARCHAR(100)       | Treatment dosage              |
| treatment_date | DATE               | Date treatment was recorded   |

## Table Relationships

The database uses primary keys and foreign keys to maintain relational integrity.

* One facility can be associated with multiple patients.
* One facility can record multiple healthcare visits.
* One patient can have multiple healthcare visits.
* One healthcare visit can have multiple diagnoses.
* One healthcare visit can have multiple treatments.

## Data Integrity

The database uses:

* Primary keys to uniquely identify records.
* A unique constraint on patient_code.
* Foreign keys to establish relationships between tables.
* NOT NULL constraints on required fields.

Relationship validation is performed using `src/validate_relationships.py`.

## Schema Implementation

The database structure is defined in:

`sql/schema.sql`

Database analysis queries are maintained in:

`sql/analysis.sql`