# HY-360 Project - Σύστημα Μισθοδοσίας

Payroll Management System για το Πανεπιστήμιο Κρήτης.

---

## Περιγραφή

Σύστημα διαχείρισης μισθοδοσίας με GUI (Tkinter) και MySQL backend. Υποστηρίζει μόνιμους και συμβασιούχους υπαλλήλους, διοικητικό και διδακτικό προσωπικό, υπολογισμό μισθών με επιδόματα, και αναφορές.

---

## Τεχνολογίες

- **Python 3**
- **MySQL/MariaDB**
- **Node.js** (για database initialization script - προαιρετικό)

---

## Εγκατάσταση

### 1. Προαπαιτούμενα

- Python 3.x
- XAMPP (ή οποιοσδήποτε MySQL server)
- MySQL Connector για Python:
  ```bash
  pip install mysql-connector-python
  ```

### 2. Setup Database

**ΣΗΜΑΝΤΙΚΟ: Κανε import με τη σειρα!**

1. Ανοίγεις XAMPP => Start MySQL
2. Ανοίγεις phpMyAdmin
3. Import το αρχείο `HY360v2UltraEdition.sql` (δημιουργεί τους πίνακες)
4. Import το αρχείο `insert_initial_data.sql` (βάζει τα departments, salaries, allowances)
5. Import το `create_views.sql` (το bonus - optional)

### 3. Configuration

Στο `database.py` (line 13-17) βάλε τα credentials σου:
```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # βάλε το password αν έχεις
    database="HY360"
)
```

### 4. Run

```bash
python main.py
```

---

## Δομή Βάσης

### Κύριοι Πίνακες:
- **employees** - Βασικά στοιχεία υπαλλήλων
- **departments** - 7 τμήματα του πανεπιστημίου
- **permanent_employees** / **contract_employees** - Τύπος απασχόλησης
- **teaching_staff** / **administrative_staff** - Κλάδος
- **contracts** - Στοιχεία συμβάσεων
- **base_salaries** - Βασικοί μισθοί
- **allowances** - Επιδόματα (οικογενειακό, έρευνας, βιβλιοθήκης)
- **payments** - Ιστορικό μισθοδοσίας

### Views (Bonus):
- **view_payroll_by_category** - Payroll ανά κατηγορία
- **view_salary_stats_by_category** - Στατιστικά μισθών
- **view_employee_payroll_details** - Λεπτομέρειες υπαλλήλου

---

## Λειτουργίες

### Διαδικασίες:
1. **Πρόσληψη Μόνιμου Υπαλλήλου**
   - Validation: hire_date πρέπει 1η μήνα, όχι μελλοντική
   - Αυτόματη εισαγωγή σε permanent_employees + teaching/admin staff

2. **Σύναψη Σύμβασης** (Συμβασιούχοι)
   - Contract start/end πρέπει 1η μήνα
   - Contract salary καθορίζεται στη σύμβαση

3. **Αλλαγή Στοιχείων Υπαλλήλου**
   - Update: οικογενειακή κατάσταση, παιδιά, τμήμα, διεύθυνση, τράπεζα

4. **Μεταβολή Μισθών/Επιδομάτων**
   - Αύξηση μόνο (όχι μείωση)
   - Temporal tracking με valid_from/valid_to

5. **Απόλυση/Συνταξιοδότηση**
   - Termination date πρέπει τελευταία μέρα μήνα

6. **Καταβολή Μισθοδοσίας**
   - Process payroll για συγκεκριμένο μήνα (YYYY-MM)
   - Υπολογισμός: base + years increase + allowances

### Αναφορές:
1. Κατάσταση μισθοδοσίας ανά κατηγορία
2. Max/Min/Avg μισθός ανά κατηγορία
3. Μέση αύξηση μισθών σε χρονική περίοδο
4. Στοιχεία συγκεκριμένου υπαλλήλου (με breakdown επιδομάτων)
5. Συνολικό ύψος μισθοδοσίας ανά κατηγορία
6. Custom SQL Query execution

---

## Υπολογισμός Μισθοδοσίας

### Για Μόνιμους:
```
Total = Base Salary + Years Increase + Family Allowance + Research/Library Allowance
```

- **Base Salary**: Από πίνακα base_salaries
- **Years Increase**: 15% * base * (years - 1), μόνο μετά το 1ο έτος
- **Family Allowance**: Για όλους (spouse + children)
- **Research Allowance**: Μόνο permanent_teaching
- **Library Allowance**: Μόνο contract_teaching

### Για Συμβασιούχους:
```
Total = Contract Salary + Family Allowance + Library Allowance (αν teaching)
```

---

## Departments

Προεγκατεστημένα 7 τμήματα:
- Βιολογίας
- Χημείας
- Φυσικής
- Επιστήμης Υπολογιστών
- Επιστήμης & Τεχνολογίας Υλικών
- Μαθηματικών & Εφαρμοσμένων Μαθηματικών
- Ιατρικής

---

## Validation Rules

- **Hire Date (Permanent)**: 1η μήνα, όχι μελλοντική
- **Hire Date (Contract)**: 1η μήνα, σήμερα ή μελλοντική
- **Contract Start**: 1η μήνα
- **Contract End**: Μετά από start (οποιαδήποτε ημερομηνία)
- **Termination Date**: Τελευταία μέρα μήνα
- **Salary Changes**: Μόνο αύξηση (no decrease)

---

## Troubleshooting

**Problem: "Database connection failed"**
- Check XAMPP MySQL is running
- Verify credentials στο database.py

**Problem: "Table doesn't exist"**
- Import το HY360v2UltraEdition.sql

**Problem: "Τα dropdowns είναι άδεια (departments, employees)"**
- Import το insert_initial_data.sql (departments + salaries + allowances)
- Για employees: πρέπει να προσθέσεις μέσω GUI

**Problem: "View not found"**
- Import το create_views.sql

**Problem: "Hire date validation fails"**
- Η ημερομηνία πρέπει να είναι 1η του μήνα
- Για μόνιμους: όχι μελλοντική
- Για συμβασιούχους: σήμερα ή μετά

---

## Notes

- Το .js αρχείο δεν χρησιμοποιείται - προτιμήστε SQL import
- Τα views είναι optional (bonus) αλλά προτεινόμενα
- Όλα τα κείμενα είναι στα ελληνικά (UTF-8)
- Default hire date: 1η τρέχοντος μήνα (για μόνιμους), 1η επόμενου μήνα (για συμβασιούχους)

---