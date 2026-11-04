-- ==========================================
-- COMMUNITY HEALTH DATA PIPELINE
-- SQL ANALYSIS
-- ==========================================


-- 1. Total number of health facilities
SELECT COUNT(*) AS total_facilities
FROM facilities;


-- 2. Total registered patients
SELECT COUNT(*) AS total_patients
FROM patients;


-- 3. Total patient visits
SELECT COUNT(*) AS total_visits
FROM visits;


-- 4. Total diagnoses recorded
SELECT COUNT(*) AS total_diagnoses
FROM diagnoses;


-- 5. Total treatments recorded
SELECT COUNT(*) AS total_treatments
FROM treatments;


-- 6. Patient distribution by gender
SELECT
    gender,
    COUNT(*) AS total_patients
FROM patients
GROUP BY gender
ORDER BY total_patients DESC;


-- 7. Patient distribution by facility
SELECT
    f.facility_name,
    f.lga,
    COUNT(p.patient_id) AS total_patients
FROM facilities f
LEFT JOIN patients p
    ON f.facility_id = p.facility_id
GROUP BY
    f.facility_id,
    f.facility_name,
    f.lga
ORDER BY total_patients DESC;


-- 8. Distribution of visits by visit type
SELECT
    visit_type,
    COUNT(*) AS total_visits
FROM visits
GROUP BY visit_type
ORDER BY total_visits DESC;


-- 9. Most frequently recorded diagnoses
SELECT
    diagnosis_name,
    COUNT(*) AS total_cases
FROM diagnoses
GROUP BY diagnosis_name
ORDER BY total_cases DESC;


-- 10. Most frequently administered treatments
SELECT
    treatment_name,
    COUNT(*) AS treatment_count
FROM treatments
GROUP BY treatment_name
ORDER BY treatment_count DESC;