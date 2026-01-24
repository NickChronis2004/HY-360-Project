-- Initial Data for HY360 Database
-- Import this after HY360v2UltraEdition.sql

USE HY360;

-- ================================================
-- DEPARTMENTS (7 τμήματα Πανεπιστημίου Κρήτης)
-- ================================================
INSERT INTO departments (department_name) VALUES
('Βιολογίας'),
('Χημείας'),
('Φυσικής'),
('Επιστήμης Υπολογιστών'),
('Επιστήμης & Τεχνολογίας Υλικών'),
('Μαθηματικών & Εφαρμοσμένων Μαθηματικών'),
('Ιατρικής');


-- ================================================
-- BASE SALARIES (Βασικοί μισθοί ανά κατηγορία)
-- ================================================
INSERT INTO base_salaries (employee_type, category, amount, valid_from, valid_to) VALUES
('permanent', 'admin', 1200.00, '2020-01-01', NULL),
('permanent', 'teaching', 1500.00, '2020-01-01', NULL),
('contract', 'admin', 1000.00, '2020-01-01', NULL),
('contract', 'teaching', 1200.00, '2020-01-01', NULL);


-- ================================================
-- ALLOWANCES (Επιδόματα)
-- ================================================
INSERT INTO allowances (allowance_type, calculation_method, price, applied_to, valid_from, valid_to) VALUES
('family', 'percentage', 0.05, 'all', '2020-01-01', NULL),
('research', 'percentage', 0.10, 'permanent_teaching', '2020-01-01', NULL),
('library', 'fixed', 100.00, 'contract_teaching', '2020-01-01', NULL);


-- ================================================
-- SAMPLE EMPLOYEES (8 υπάλληλοι - όλοι οι συνδυασμοί)
-- ================================================

-- 1. Μόνιμος Διοικητικός (άγαμος, χωρίς παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Γιώργος', 'Παπαδόπουλος', 'single', 0, 1, '2020-01-01', 'Ηράκλειο, Κρήτης', '6971111111', 'GR1234567890', 'Εθνική', 'active');
INSERT INTO permanent_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO administrative_staff (employee_id) VALUES (LAST_INSERT_ID());

-- 2. Μόνιμος Διοικητικός (έγγαμος, 2 παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Μαρία', 'Αλεξίου', 'married', 2, 2, '2018-01-01', 'Ρέθυμνο, Κρήτης', '6972222222', 'GR2345678901', 'Πειραιώς', 'active');
INSERT INTO permanent_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO administrative_staff (employee_id) VALUES (LAST_INSERT_ID());

-- 3. Μόνιμος Διδακτικός (άγαμος, χωρίς παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Νίκος', 'Καζαντζάκης', 'single', 0, 4, '2019-01-01', 'Χανιά, Κρήτης', '6973333333', 'GR3456789012', 'Alpha Bank', 'active');
INSERT INTO permanent_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO teaching_staff (employee_id) VALUES (LAST_INSERT_ID());

-- 4. Μόνιμος Διδακτικός (έγγαμος, 3 παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Ελένη', 'Βενιζέλου', 'married', 3, 7, '2015-01-01', 'Ηράκλειο, Κρήτης', '6974444444', 'GR4567890123', 'Eurobank', 'active');
INSERT INTO permanent_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO teaching_staff (employee_id) VALUES (LAST_INSERT_ID());

-- 5. Συμβασιούχος Διοικητικός (άγαμος, χωρίς παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Δημήτρης', 'Μακρής', 'single', 0, 3, '2024-01-01', 'Ηράκλειο, Κρήτης', '6975555555', 'GR5678901234', 'Εθνική', 'active');
INSERT INTO contract_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO administrative_staff (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO contracts (employee_id, contract_start, contract_end, contract_salary, employee_status)
VALUES (LAST_INSERT_ID(), '2024-01-01', '2025-12-31', 1000.00, 'active');

-- 6. Συμβασιούχος Διοικητικός (έγγαμος, 1 παιδί)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Σοφία', 'Κωνσταντίνου', 'married', 1, 5, '2023-01-01', 'Ρέθυμνο, Κρήτης', '6976666666', 'GR6789012345', 'Πειραιώς', 'active');
INSERT INTO contract_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO administrative_staff (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO contracts (employee_id, contract_start, contract_end, contract_salary, employee_status)
VALUES (LAST_INSERT_ID(), '2023-01-01', '2025-06-30', 1100.00, 'active');

-- 7. Συμβασιούχος Διδακτικός (άγαμος, χωρίς παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Αντώνης', 'Σαμαράς', 'single', 0, 6, '2024-01-01', 'Χανιά, Κρήτης', '6977777777', 'GR7890123456', 'Alpha Bank', 'active');
INSERT INTO contract_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO teaching_staff (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO contracts (employee_id, contract_start, contract_end, contract_salary, employee_status)
VALUES (LAST_INSERT_ID(), '2024-01-01', '2025-12-31', 1200.00, 'active');

-- 8. Συμβασιούχος Διδακτικός (έγγαμος, 2 παιδιά)
INSERT INTO employees (firstname, lastname, marital_status, num_children, department_id, hire_date, address, phone, bank_account, bank_name, employee_status)
VALUES ('Κατερίνα', 'Παπανδρέου', 'married', 2, 4, '2022-01-01', 'Ηράκλειο, Κρήτης', '6978888888', 'GR8901234567', 'Eurobank', 'active');
INSERT INTO contract_employees (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO teaching_staff (employee_id) VALUES (LAST_INSERT_ID());
INSERT INTO contracts (employee_id, contract_start, contract_end, contract_salary, employee_status)
VALUES (LAST_INSERT_ID(), '2022-01-01', '2026-12-31', 1300.00, 'active');


-- ================================================
-- SAMPLE PAYMENTS (Ιστορικό μισθοδοσίας για demo)
-- ================================================

-- Πληρωμές Ιανουαρίου 2025 για όλους
INSERT INTO payments (employee_id, payment_date, reference_month, base_salary, years_increase, family_allowance, research_allowance, library_allowance, total_amount) VALUES
(1, '2025-01-31', '2025-01', 1200.00, 720.00, 0.00, 0.00, 0.00, 1920.00),      -- Μόνιμος Διοικητικός 5 χρόνια
(2, '2025-01-31', '2025-01', 1200.00, 1080.00, 180.00, 0.00, 0.00, 2460.00),   -- Μόνιμος Διοικητικός 7 χρόνια, έγγαμος+2παιδιά
(3, '2025-01-31', '2025-01', 1500.00, 675.00, 0.00, 150.00, 0.00, 2325.00),    -- Μόνιμος Διδακτικός 6 χρόνια
(4, '2025-01-31', '2025-01', 1500.00, 1350.00, 300.00, 150.00, 0.00, 3300.00), -- Μόνιμος Διδακτικός 10 χρόνια, έγγαμος+3παιδιά
(5, '2025-01-31', '2025-01', 1000.00, 0.00, 0.00, 0.00, 0.00, 1000.00),        -- Συμβασιούχος Διοικητικός
(6, '2025-01-31', '2025-01', 1100.00, 0.00, 110.00, 0.00, 0.00, 1210.00),      -- Συμβασιούχος Διοικητικός, έγγαμος+1παιδί
(7, '2025-01-31', '2025-01', 1200.00, 0.00, 0.00, 0.00, 100.00, 1300.00),      -- Συμβασιούχος Διδακτικός
(8, '2025-01-31', '2025-01', 1300.00, 0.00, 195.00, 0.00, 100.00, 1595.00);    -- Συμβασιούχος Διδακτικός, έγγαμος+2παιδιά


-- ================================================
-- Επιβεβαίωση
-- ================================================
SELECT 'Departments:', COUNT(*) FROM departments;
SELECT 'Base Salaries:', COUNT(*) FROM base_salaries;
SELECT 'Allowances:', COUNT(*) FROM allowances;
SELECT 'Employees:', COUNT(*) FROM employees;
SELECT 'Permanent:', COUNT(*) FROM permanent_employees;
SELECT 'Contract:', COUNT(*) FROM contract_employees;
SELECT 'Teaching:', COUNT(*) FROM teaching_staff;
SELECT 'Admin:', COUNT(*) FROM administrative_staff;
SELECT 'Contracts:', COUNT(*) FROM contracts;
SELECT 'Payments:', COUNT(*) FROM payments;
