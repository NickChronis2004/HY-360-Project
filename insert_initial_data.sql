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
('permanent', 'permanent_admin', 1200.00, '2020-01-01', NULL),
('permanent', 'permanent_teaching', 1500.00, '2020-01-01', NULL),
('contract', 'contract_admin', 1000.00, '2020-01-01', NULL),
('contract', 'contract_teaching', 1200.00, '2020-01-01', NULL);


-- ================================================
-- ALLOWANCES (Επιδόματα)
-- ================================================

-- Οικογενειακό επίδομα (percentage based)
INSERT INTO allowances (allowance_type, calculation_method, price, applied_to, valid_from, valid_to) VALUES
('family', 'percentage', 0.05, 'all', '2020-01-01', NULL);

-- Επίδομα έρευνας (για permanent_teaching)
INSERT INTO allowances (allowance_type, calculation_method, price, applied_to, valid_from, valid_to) VALUES
('research', 'percentage', 0.10, 'permanent_teaching', '2020-01-01', NULL);

-- Επίδομα βιβλιοθήκης (για contract_teaching)
INSERT INTO allowances (allowance_type, calculation_method, price, applied_to, valid_from, valid_to) VALUES
('library', 'fixed', 100.00, 'contract_teaching', '2020-01-01', NULL);


-- ================================================
-- Επιβεβαίωση
-- ================================================
SELECT 'Departments:', COUNT(*) FROM departments;
SELECT 'Base Salaries:', COUNT(*) FROM base_salaries;
SELECT 'Allowances:', COUNT(*) FROM allowances;
