-- 1. Health Facilities
CREATE TABLE IF NOT EXISTS facilities (
    facility_id SERIAL PRIMARY KEY,
    facility_name VARCHAR(150) NOT NULL,
    state VARCHAR(100),
    lga VARCHAR(100),
    facility_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Patients
CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    patient_code VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(20),
    date_of_birth DATE,
    facility_id INTEGER REFERENCES facilities(facility_id),
    registration_date DATE DEFAULT CURRENT_DATE
);

-- 3. Health Visits
CREATE TABLE IF NOT EXISTS visits (
    visit_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(patient_id),
    facility_id INTEGER REFERENCES facilities(facility_id),
    visit_date DATE NOT NULL,
    visit_type VARCHAR(50),
    symptoms TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Diagnoses
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id SERIAL PRIMARY KEY,
    visit_id INTEGER REFERENCES visits(visit_id),
    diagnosis_name VARCHAR(150) NOT NULL,
    diagnosis_code VARCHAR(50),
    diagnosis_date DATE DEFAULT CURRENT_DATE
);

-- 5. Treatments
CREATE TABLE IF NOT EXISTS treatments (
    treatment_id SERIAL PRIMARY KEY,
    visit_id INTEGER REFERENCES visits(visit_id),
    treatment_name VARCHAR(150) NOT NULL,
    dosage VARCHAR(100),
    treatment_date DATE DEFAULT CURRENT_DATE
);