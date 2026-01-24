
USE HY360;

-- VIEW 1: Payroll by Category
-- Κατάσταση μισθοδοσίας ανά κατηγορία
CREATE OR REPLACE VIEW view_payroll_by_category AS
SELECT
    CASE
        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
        ELSE 'unknown'
    END AS category,
    p.reference_month,
    SUM(p.total_amount) AS total_amount,
    COUNT(DISTINCT p.employee_id) AS num_employees
FROM payments p
JOIN employees e ON p.employee_id = e.employee_id
LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
GROUP BY category, p.reference_month;


-- VIEW 2: Salary Statistics by Category
-- Μέγιστος/Ελάχιστος/Μέσος μισθός ανά κατηγορία
CREATE OR REPLACE VIEW view_salary_stats_by_category AS
SELECT
    CASE
        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
        ELSE 'unknown'
    END AS category,
    p.reference_month,
    MAX(p.total_amount) AS max_salary,
    MIN(p.total_amount) AS min_salary,
    AVG(p.total_amount) AS avg_salary
FROM payments p
JOIN employees e ON p.employee_id = e.employee_id
LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
GROUP BY category, p.reference_month;


-- VIEW 3: Employee Details with Payroll History
-- Στοιχεία υπαλλήλου με ιστορικό μισθοδοσίας
CREATE OR REPLACE VIEW view_employee_payroll_details AS
SELECT
    e.employee_id,
    e.firstname,
    e.lastname,
    e.marital_status,
    e.num_children,
    e.hire_date,
    e.employee_status,
    d.department_name,
    CASE
        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
        ELSE 'unknown'
    END AS category,
    p.payment_date,
    p.reference_month,
    p.base_salary,
    p.years_increase,
    p.family_allowance,
    p.research_allowance,
    p.library_allowance,
    p.total_amount
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id
LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
LEFT JOIN payments p ON p.employee_id = e.employee_id
ORDER BY e.employee_id, p.payment_date DESC;

-- Test View 1
-- SELECT * FROM view_payroll_by_category ORDER BY reference_month DESC, category;

-- Test View 2
-- SELECT * FROM view_salary_stats_by_category ORDER BY reference_month DESC, category;

-- Test View 3
-- SELECT * FROM view_employee_payroll_details WHERE employee_id = 1;
