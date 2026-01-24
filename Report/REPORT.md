# HY-360 Project Report
## Σύστημα Μισθοδοσίας Πανεπιστημίου Κρήτης

---

## 1. Περιγραφή Συστήματος

Το σύστημα διαχειρίζεται τη μισθοδοσία του προσωπικού του Πανεπιστημίου Κρήτης. Υποστηρίζει:

- **Δύο τύπους απασχόλησης**: Μόνιμοι και Συμβασιούχοι υπάλληλοι
- **Δύο κλάδους προσωπικού**: Διοικητικό και Διδακτικό
- **Αυτόματο υπολογισμό μισθοδοσίας** με βασικό μισθό, προσαυξήσεις ετών, και επιδόματα
- **Temporal tracking** για αλλαγές μισθών και επιδομάτων
- **Αναφορές και στατιστικά** μέσω SQL Views

### Τεχνολογίες
- **Backend**: Python 3 + MySQL/MariaDB
- **Frontend**: Tkinter GUI
- **Database**: MySQL με mysql-connector-python

---

## 2. Entity-Relationship Diagram (ER)

### 2.1 Οντότητες (Entities)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              EMPLOYEES                                      │
│            (Κεντρική οντότητα - Generalization/Specialization)              │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: employee_id                                                            │
│  firstname, lastname, marital_status, num_children                          │
│  hire_date, termination_date, address, phone                                │
│  bank_account, bank_name, employee_status                                   │
│  FK: department_id → DEPARTMENTS                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                                       │
                    │ ISA (d,t)                             │ ISA (d,t)
                    │ Employment Type                       │ Staff Category
                    ▼                                       ▼
    ┌───────────────┴───────────────┐       ┌───────────────┴───────────────┐
    │                               │       │                               │
    ▼                               ▼       ▼                               ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐   ┌─────────────────── ┐
│PERMANENT_EMPLOYEES│   │ CONTRACT_EMPLOYEES│   │  TEACHING_STAFF   │   │ADMINISTRATIVE_STAFF│
├───────────────────┤   ├───────────────────┤   ├───────────────────┤   ├─────────────────── ┤
│ PK/FK: employee_id│   │ PK/FK: employee_id│   │ PK/FK: employee_id│   │ PK/FK: employee_id │
└───────────────────┘   └─────────┬─────────┘   └───────────────────┘   └─────────────────── ┘
                                  │
                                  │ 1:N
                                  ▼
                        ┌───────────────────┐
                        │     CONTRACTS     │
                        ├───────────────────┤
                        │ PK: contract_id   │
                        │ FK: employee_id   │
                        │ contract_start    │
                        │ contract_end      │
                        │ contract_salary   │
                        │ employee_status   │
                        └───────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              DEPARTMENTS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: department_id                                                          │
│  department_name (UNIQUE)                                                   │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              BASE_SALARIES                                  │
│  (Temporal entity - valid_from/valid_to)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: base_salary_id                                                         │
│  employee_type (permanent/contract)                                         │
│  category (admin/teaching)                                                  │
│  amount                                                                     │
│  valid_from, valid_to                                                       │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              ALLOWANCES                                     │
│  (Temporal entity - valid_from/valid_to)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: allowance_id                                                           │
│  allowance_type (family/research/library)                                   │
│  calculation_method (percentage/fixed)                                      │
│  price                                                                      │
│  applied_to (all/permanent_teaching/contract_teaching)                      │
│  valid_from, valid_to                                                       │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              PAYMENTS                                       │
│  (Transaction/History entity)                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  PK: payment_id                                                             │
│  FK: employee_id → EMPLOYEES                                                │
│  payment_date, reference_month                                              │
│  base_salary, years_increase                                                │
│  family_allowance, research_allowance, library_allowance                    │
│  total_amount                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Σχέσεις (Relationships)

| Σχέση | Τύπος | Περιγραφή |
|-------|-------|-----------|
| EMPLOYEES → DEPARTMENTS | N:1 | Κάθε υπάλληλος ανήκει σε ένα τμήμα |
| EMPLOYEES → PERMANENT_EMPLOYEES | 1:1 (ISA) | Specialization - Μόνιμος υπάλληλος |
| EMPLOYEES → CONTRACT_EMPLOYEES | 1:1 (ISA) | Specialization - Συμβασιούχος |
| EMPLOYEES → TEACHING_STAFF | 1:1 (ISA) | Specialization - Διδακτικό προσωπικό |
| EMPLOYEES → ADMINISTRATIVE_STAFF | 1:1 (ISA) | Specialization - Διοικητικό προσωπικό |
| CONTRACT_EMPLOYEES → CONTRACTS | 1:N | Κάθε συμβασιούχος έχει πολλές συμβάσεις |
| EMPLOYEES → PAYMENTS | 1:N | Κάθε υπάλληλος έχει πολλές πληρωμές |

### 2.3 ISA Hierarchies (Ορθογώνιες Διαστάσεις)

Κάθε υπάλληλος κατηγοριοποιείται σε **δύο ανεξάρτητες διαστάσεις**:

**1. Employment Type (Disjoint, Total)** - Σχέση Εργασίας:
- EMPLOYEES → PERMANENT_EMPLOYEES ή CONTRACT_EMPLOYEES
- Κάθε υπάλληλος είναι ΑΚΡΙΒΩΣ ένας τύπος (Μόνιμος XOR Συμβασιούχος)

**2. Staff Category (Disjoint, Total)** - Κλάδος:
- EMPLOYEES → TEACHING_STAFF ή ADMINISTRATIVE_STAFF
- Κάθε υπάλληλος είναι ΑΚΡΙΒΩΣ ένας κλάδος (Διδακτικός XOR Διοικητικός)

**ΣΗΜΑΝΤΙΚΟ**: Και τα δύο ISA συνδέονται απευθείας στο EMPLOYEES, ΟΧΙ το ένα κάτω από το άλλο.
Αυτό επιτρέπει όλους τους συνδυασμούς: Μόνιμος Διδακτικός, Μόνιμος Διοικητικός, Συμβασιούχος Διδακτικός, Συμβασιούχος Διοικητικός.

---

## 3. Relational Schema

```sql
DEPARTMENTS (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(50) UNIQUE NOT NULL
)

EMPLOYEES (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    marital_status VARCHAR(50) NOT NULL,        -- 'single' | 'married'
    num_children INT DEFAULT 0,
    department_id INT NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE DEFAULT NULL,          -- Ημερομηνία απόλυσης/συνταξιοδότησης
    address VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    bank_account VARCHAR(40) NOT NULL,
    bank_name VARCHAR(50),
    employee_status VARCHAR(20) NOT NULL,        -- 'active' | 'terminated'
    FOREIGN KEY (department_id) REFERENCES DEPARTMENTS(department_id)
)

PERMANENT_EMPLOYEES (
    employee_id INT PRIMARY KEY,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id) ON DELETE CASCADE
)

CONTRACT_EMPLOYEES (
    employee_id INT PRIMARY KEY,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id) ON DELETE CASCADE
)

TEACHING_STAFF (
    employee_id INT PRIMARY KEY,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id) ON DELETE CASCADE
)

ADMINISTRATIVE_STAFF (
    employee_id INT PRIMARY KEY,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id) ON DELETE CASCADE
)

CONTRACTS (
    contract_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    contract_start DATE NOT NULL,
    contract_end DATE NOT NULL,
    contract_salary FLOAT NOT NULL,
    employee_status VARCHAR(20) NOT NULL,        -- 'active' | 'terminated'
    FOREIGN KEY (employee_id) REFERENCES CONTRACT_EMPLOYEES(employee_id)
)

BASE_SALARIES (
    base_salary_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_type VARCHAR(50) NOT NULL,          -- 'permanent' | 'contract'
    category VARCHAR(50) NOT NULL,               -- 'admin' | 'teaching'
    amount FLOAT NOT NULL,
    valid_from DATE NOT NULL,
    valid_to DATE DEFAULT NULL                   -- NULL = ισχύει ακόμα
)

ALLOWANCES (
    allowance_id INT PRIMARY KEY AUTO_INCREMENT,
    allowance_type VARCHAR(50) NOT NULL,         -- 'family' | 'research' | 'library'
    calculation_method VARCHAR(50) NOT NULL,     -- 'percentage' | 'fixed'
    price FLOAT NOT NULL,
    applied_to VARCHAR(50) NOT NULL,             -- 'all' | 'permanent_teaching' | 'contract_teaching'
    valid_from DATE NOT NULL,
    valid_to DATE DEFAULT NULL
)

PAYMENTS (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    payment_date DATE NOT NULL,
    reference_month VARCHAR(50) NOT NULL,        -- 'YYYY-MM'
    base_salary FLOAT NOT NULL,
    years_increase FLOAT DEFAULT 0,
    family_allowance FLOAT DEFAULT 0,
    research_allowance FLOAT DEFAULT 0,
    library_allowance FLOAT DEFAULT 0,
    total_amount FLOAT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
)
```

---

## 4. Κανόνες Επιχειρησιακής Λογικής (Business Rules)

### 4.1 Validation Rules

| Πεδίο | Κανόνας |
|-------|---------|
| Hire Date (Permanent) | Πρέπει να είναι 1η μήνα, ΟΧΙ μελλοντική |
| Hire Date (Contract) | Πρέπει να είναι 1η μήνα, σήμερα ή μελλοντική |
| Contract Start | Πρέπει να είναι 1η μήνα |
| Contract End | Μετά από contract_start (οποιαδήποτε ημερομηνία) |
| Termination Date | Πρέπει να είναι τελευταία μέρα μήνα |
| Salary Changes | Μόνο αύξηση επιτρέπεται (no decrease) |

### 4.2 Υπολογισμός Μισθοδοσίας

**Για Μόνιμους Υπαλλήλους:**
```
Total = Base Salary
      + Years Increase (15% × base × (years-1), αν years > 1)
      + Family Allowance (5% × base × (1 + num_children), αν married)
      + Research Allowance (10% × base, μόνο για teaching)
```

**Για Συμβασιούχους:**
```
Total = Contract Salary
      + Family Allowance (5% × contract_salary × (1 + num_children), αν married)
      + Library Allowance (100€ fixed, μόνο για teaching)
```

### 4.3 Payroll Processing

- Οι υπάλληλοι που απολύθηκαν ΜΕΣΑ στον μήνα πληρώνονται κανονικά
- Η μισθοδοσία τρέχει μία φορά τον μήνα
- Αποθηκεύεται πλήρες breakdown στον πίνακα PAYMENTS

---

## 5. Λειτουργίες Συστήματος

### 5.1 Διαδικασίες (Procedures)

1. **Πρόσληψη Μόνιμου Υπαλλήλου**
   - Εισαγωγή σε: employees, permanent_employees, teaching/administrative_staff

2. **Σύναψη Σύμβασης**
   - Εισαγωγή σε: employees, contract_employees, teaching/administrative_staff, contracts

3. **Αλλαγή Στοιχείων Υπαλλήλου**
   - Update: marital_status, num_children, department_id, address, phone, bank details

4. **Μεταβολή Μισθών/Επιδομάτων**
   - Temporal update με valid_from/valid_to στους πίνακες base_salaries/allowances

5. **Απόλυση/Συνταξιοδότηση**
   - Update employee_status = 'terminated', termination_date

6. **Καταβολή Μισθοδοσίας**
   - Process όλων των active + terminated-this-month υπαλλήλων
   - Αποθήκευση στον πίνακα payments

### 5.2 Αναφορές (Reports)

1. Κατάσταση μισθοδοσίας ανά κατηγορία
2. Max/Min/Avg μισθός ανά κατηγορία
3. Μέση αύξηση μισθών σε χρονική περίοδο
4. Στοιχεία συγκεκριμένου υπαλλήλου (με breakdown)
5. Συνολικό ύψος μισθοδοσίας ανά κατηγορία
6. Custom SQL Query

---

## 6. SQL Views (Bonus)

```sql
-- View 1: Payroll by Category
CREATE VIEW view_payroll_by_category AS
SELECT
    reference_month,
    CASE
        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
    END AS category,
    SUM(total_amount) AS total_amount
FROM payments p
JOIN employees e ON p.employee_id = e.employee_id
LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
GROUP BY reference_month, category;

-- View 2: Salary Statistics by Category
CREATE VIEW view_salary_stats_by_category AS
SELECT
    reference_month,
    category,
    MAX(total_amount) AS max_salary,
    MIN(total_amount) AS min_salary,
    AVG(total_amount) AS avg_salary
FROM view_payroll_by_category
GROUP BY reference_month, category;

-- View 3: Employee Payroll Details
CREATE VIEW view_employee_payroll_details AS
SELECT
    e.*,
    p.payment_date, p.reference_month, p.base_salary,
    p.years_increase, p.family_allowance,
    p.research_allowance, p.library_allowance, p.total_amount
FROM employees e
LEFT JOIN payments p ON e.employee_id = p.employee_id;
```

**Σημείωση**: Τα views είναι optional. Οι αναφορές έχουν fallback queries αν τα views δεν υπάρχουν.

---

## 7. Κατηγορίες Υπαλλήλων (Sample Data)

| # | Ονοματεπώνυμο | Τύπος | Κλάδος | Κατάσταση | Μισθός |
|---|---------------|-------|--------|-----------|--------|
| 1 | Γιώργος Παπαδόπουλος | Μόνιμος | Διοικητικός | single, 0 παιδιά | 1920€ |
| 2 | Μαρία Αλεξίου | Μόνιμος | Διοικητικός | married, 2 παιδιά | 2460€ |
| 3 | Νίκος Καζαντζάκης | Μόνιμος | Διδακτικός | single, 0 παιδιά | 2325€ |
| 4 | Ελένη Βενιζέλου | Μόνιμος | Διδακτικός | married, 3 παιδιά | 3300€ |
| 5 | Δημήτρης Μακρής | Συμβασιούχος | Διοικητικός | single, 0 παιδιά | 1000€ |
| 6 | Σοφία Κωνσταντίνου | Συμβασιούχος | Διοικητικός | married, 1 παιδί | 1210€ |
| 7 | Αντώνης Σαμαράς | Συμβασιούχος | Διδακτικός | single, 0 παιδιά | 1300€ |
| 8 | Κατερίνα Παπανδρέου | Συμβασιούχος | Διδακτικός | married, 2 παιδιά | 1595€ |

---

## 8. Αρχεία Έργου

| Αρχείο | Περιγραφή |
|--------|-----------|
| `main.py` | Tkinter GUI application |
| `database.py` | Database Manager class με όλες τις SQL operations |
| `HY360v2UltraEdition.sql` | Schema creation (tables, indexes, constraints) |
| `insert_initial_data.sql` | Initial data (departments, salaries, allowances, sample employees) |
| `create_views.sql` | SQL Views (bonus) |
| `README.md` | Documentation |
| `REPORT.md` | Αυτή η αναφορά |

---

## 9. Οδηγίες Εγκατάστασης

1. **Start MySQL** (XAMPP ή standalone)
2. **Import με τη σειρά**:
   ```
   1. HY360v2UltraEdition.sql  (schema)
   2. insert_initial_data.sql  (data)
   3. create_views.sql         (optional bonus)
   ```
3. **Configure** `database.py` (credentials)
4. **Run**: `python main.py`

---

## 10. Διάγραμμα ER (Graphical)

Για graphical ER diagram, μπορείς να χρησιμοποιήσεις:
- **draw.io** (diagrams.net)
- **MySQL Workbench** (reverse engineering)
- **Lucidchart**

### Suggested Layout:

```
                                    ┌──────────────┐
                                    │ DEPARTMENTS  │
                                    └──────┬───────┘
                                           │ 1
                                           │ N
                              ┌────────────┴────────────┐
                              │        EMPLOYEES        │
                              └────────────┬────────────┘
                                    /      │      \
                   ISA (d,t)       /       │       \      ISA (d,t)
                Employment Type  /         │         \   Staff Category
                               /           │           \
              ┌───────────────┐ ┌─────────────────┐ ┌───────────────┐
              │   PERMANENT   │ │    CONTRACT     │ │   TEACHING    │ ┌───────────────┐
              │   EMPLOYEES   │ │    EMPLOYEES    │ │    STAFF      │ │    ADMIN      │
              └───────────────┘ └────────┬────────┘ └───────────────┘ │    STAFF      │
                                         │ 1:N                        └───────────────┘
                                ┌────────┴────────┐
                                │    CONTRACTS    │
                                └─────────────────┘

    ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
    │BASE_SALARIES│      │ ALLOWANCES  │      │  PAYMENTS   │
    └─────────────┘      └─────────────┘      └─────────────┘
```

**ΣΗΜΑΝΤΙΚΟ**: Τα δύο ISA τρίγωνα ξεκινούν και τα δύο από το EMPLOYEES (παράλληλα),
επιτρέποντας όλους τους συνδυασμούς (π.χ. Συμβασιούχος Διδακτικός).

---

*Τέλος Αναφοράς*
