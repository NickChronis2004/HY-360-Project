import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """connect to database"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="HY360",
                autocommit=True
            )
            if self.connection.is_connected():
                print(" Database connected")
        except Error as e:
            print(f" Connection error: {e}")


    def get_departments(self):
        '''
        Λίστα με όλα τα τμήματα
        
        @return: list of dict - {department_id, department_name}
        '''
        cursor = None
        try:
            cursor = self.connection.cursor()
            
            query = '''
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_name
            '''
            
            cursor.execute(query)
            departments = [
                {"department_id": row[0], "department_name": row[1]}
                for row in cursor.fetchall()
            ]
            
            return departments
            
        except Error as e:
            print(f" Error fetching departments: {e}")
            return []
        finally:
            if cursor:
                cursor.close()



    def get_active_employees(self):
        '''
        λιστα με ενεργους υπαλληλους (χωρις απολυμενους)
        
        @return: list of dict - μόνο ενεργοί υπάλληλοι
        '''
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    e.employee_id,
                    e.firstname,
                    e.lastname,
                    e.department_id,
                    d.department_name AS department_name,
                    e.hire_date,
                    e.employee_status
                FROM employees e
                JOIN departments d ON e.department_id = d.department_id
                WHERE e.employee_status = 'active'
                ORDER BY e.lastname, e.firstname
            """
            
            cursor.execute(query)
            employees = cursor.fetchall()
            
            return employees
            
        except Error as e:
            print(f" Error fetching active employees: {e}")
            return []
        finally:
            if cursor:
                cursor.close()



    def hire_permanent_employee(self, data):
        '''
        προσληψη μονιμου υπαλληλου
        @param data: dict με στοιχεία υπαλλήλου
            - name: str - πλήρες όνομα
            - marital_status: str - 'single' ή 'married'
            - num_children: int - αριθμός παιδιών
            - category: str - 'permanent_admin' ή 'permanent_teaching'
            - department: str - τμήμα εργασίας
            - hire_date: str - ημερομηνία πρόσληψης (YYYY-MM-DD)
            - address: str - διεύθυνση κατοικίας
            - phone: str - τηλέφωνο
            - bank_account: str - αριθμός τραπεζικού λογαριασμού
            - bank_name: str - όνομα τράπεζας
        @return: int - employee_id του νέου υπαλλήλου ή None αν αποτύχει
        '''
        cursor = None
        try:
            hire_date_raw = (data.get('hire_date') or '').strip()
            hire_date = datetime.strptime(hire_date_raw, '%Y-%m-%d').date()
            today = datetime.now().date()
            if hire_date.day != 1 or hire_date > today:
                return None

            category = data.get('category')
            if category not in ('permanent_admin', 'permanent_teaching'):
                return None

            cursor = self.connection.cursor()
            self.connection.start_transaction()

            query = '''
                INSERT INTO employees (
                firstname, 
                lastname, 
                marital_status, 
                num_children, 
                department_id, 
                hire_date, 
                address, 
                phone, 
                bank_account, 
                bank_name, 
                employee_status
            ) VALUES(%(firstname)s, %(lastname)s, %(marital_status)s, %(num_children)s, %(department_id)s, %(hire_date)s, %(address)s, %(phone)s, %(bank_account)s, %(bank_name)s, 'active')
            '''

            cursor.execute(query, data)
            new_id = cursor.lastrowid

            cursor.execute(
                'INSERT INTO permanent_employees (employee_id) VALUES (%s)',
                (new_id,)
            )

            if category == 'permanent_admin':
                cursor.execute(
                    'INSERT INTO administrative_staff (employee_id) VALUES (%s)',
                    (new_id,)
                )
            else:
                cursor.execute(
                    'INSERT INTO teaching_staff (employee_id) VALUES (%s)',
                    (new_id,)
                )

            self.connection.commit()
            return new_id
        except (Error, ValueError) as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error hiring new employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    

    def hire_contract_employee(self, data):
        '''
        προσληψη υπαλληλου με συμβαση
        
        @param data: dict με στοιχεία υπαλλήλου
            - name: str - πλήρες όνομα
            - marital_status: str - 'single' ή 'married'
            - num_children: int - αριθμός παιδιών
            - category: str - 'contract_admin' ή 'contract_teaching'
            - department: str - τμήμα εργασίας
            - hire_date: str - ημερομηνία πρόσληψης (YYYY-MM-DD)
            - address: str - διεύθυνση κατοικίας
            - phone: str - τηλέφωνο
            - bank_account: str - αριθμός τραπεζικού λογαριασμού
            - bank_name: str - όνομα τράπεζας
            - contract_start: str - ημερομηνία έναρξης σύμβασης (YYYY-MM-DD)
            - contract_end: str - ημερομηνία λήξης σύμβασης (YYYY-MM-DD)
            - contract_salary: float - μισθός σύμβασης
        @return: int - employee_id του νέου υπαλλήλου ή None αν αποτύχει
        '''
        cursor = None
        try:
            hire_date_raw = (data.get('hire_date') or '').strip()
            contract_start_raw = (data.get('contract_start') or '').strip()
            contract_end_raw = (data.get('contract_end') or '').strip()

            hire_date = datetime.strptime(hire_date_raw, '%Y-%m-%d').date()
            contract_start = datetime.strptime(contract_start_raw, '%Y-%m-%d').date()
            contract_end = datetime.strptime(contract_end_raw, '%Y-%m-%d').date()

            today = datetime.now().date()
            if hire_date.day != 1 or contract_start.day != 1:
                return None
            if hire_date < today or contract_start < today:
                return None
            if contract_start < hire_date:
                return None
            if contract_end < contract_start:
                return None

            contract_salary = float(data.get('contract_salary'))
            if contract_salary <= 0:
                return None

            category = data.get('category')
            if category not in ('contract_admin', 'contract_teaching'):
                return None

            cursor = self.connection.cursor()
            self.connection.start_transaction()

            query = '''
                INSERT INTO employees (
                firstname, 
                lastname, 
                marital_status, 
                num_children, 
                department_id, 
                hire_date, 
                address, 
                phone, 
                bank_account, 
                bank_name, 
                employee_status
            ) VALUES(%(firstname)s, %(lastname)s, %(marital_status)s, %(num_children)s, %(department_id)s, %(hire_date)s, %(address)s, %(phone)s, %(bank_account)s, %(bank_name)s, 'active')
            '''

            cursor.execute(query, data)
            new_id = cursor.lastrowid

            cursor.execute(
                'INSERT INTO contract_employees (employee_id) VALUES (%s)',
                (new_id,)
            )

            cursor.execute(
                '''
                INSERT INTO contracts (
                    employee_id,
                    contract_start,
                    contract_end,
                    contract_salary,
                    employee_status
                ) VALUES (%s, %s, %s, %s, 'active')
                ''',
                (new_id, contract_start, contract_end, contract_salary)
            )

            if category == 'contract_admin':
                cursor.execute(
                    'INSERT INTO administrative_staff (employee_id) VALUES (%s)',
                    (new_id,)
                )
            else:
                cursor.execute(
                    'INSERT INTO teaching_staff (employee_id) VALUES (%s)',
                    (new_id,)
                )

            self.connection.commit()
            return new_id
        except (Error, ValueError, TypeError) as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error hiring new contract employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    

    def update_employee(self, employee_id, data):
        '''
        ενημερωση στοιχειων υπαλληλου
        
        @param employee_id: int - το ID του υπαλλήλου προς ενημέρωση
        @param data: dict με στοιχεία προς αλλαγή (μπορεί να περιέχει οποιοδήποτε από τα πεδία του υπαλλήλου)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        cursor = None
        try:
            if not data:
                return True

            allowed_fields = {
                'firstname',
                'lastname',
                'marital_status',
                'num_children',
                'department_id',
                'hire_date',
                'address',
                'phone',
                'bank_account',
                'bank_name',
                'employee_status',
            }
            clean_data = {k: v for k, v in data.items() if k in allowed_fields}
            if not clean_data:
                return True

            set_clause = []
            values = []
            for key, value in clean_data.items():
                set_clause.append(f"{key} = %s")
                values.append(value)
            values.append(employee_id)

            cursor = self.connection.cursor()
            query = f"UPDATE employees SET {', '.join(set_clause)} WHERE employee_id = %s"
            cursor.execute(query, tuple(values))
            self.connection.commit()
            return True
        except Exception as e:
            print(f" Error updating employee {employee_id}: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    

    

    def update_base_salaries(self, category_code, new_amount):
        '''
        ενημερωση βασικου μισθου
        
        @param category_code: str - κατηγορία προσωπικού ('permanent_admin', 'permanent_teaching', 'contract_admin', 'contract_teaching')
        @param new_amount: float - νέο ποσό βασικού μισθού (δεν επιτρέπεται μείωση)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        cursor = None
        try:
            amount = float(new_amount)
            if amount <= 0:
                return False

            if not category_code or '_' not in category_code:
                return False
            employee_type, category = category_code.split('_', 1)
            if employee_type not in ('permanent', 'contract'):
                return False
            if category not in ('admin', 'teaching'):
                return False

            today = datetime.now().date()

            cursor = self.connection.cursor(dictionary=True)
            self.connection.start_transaction()

            cursor.execute(
                """
                SELECT base_salary_id, amount
                FROM base_salaries
                WHERE employee_type = %s
                  AND category = %s
                  AND valid_to IS NULL
                ORDER BY valid_from DESC
                LIMIT 1
                """,
                (employee_type, category)
            )
            row = cursor.fetchone()

            if row:
                current_amount = float(row['amount'])
                if amount < current_amount:
                    self.connection.rollback()
                    return False
                if amount == current_amount:
                    self.connection.rollback()
                    return True

                cursor.execute(
                    "UPDATE base_salaries SET valid_to = %s WHERE base_salary_id = %s",
                    (today, row['base_salary_id'])
                )

            cursor.execute(
                """
                INSERT INTO base_salaries (
                    employee_type,
                    category,
                    amount,
                    valid_from,
                    valid_to
                ) VALUES (%s, %s, %s, %s, NULL)
                """,
                (employee_type, category, amount, today)
            )

            self.connection.commit()
            return True
        except (Error, ValueError, TypeError) as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error updating base salary: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    

    def update_allowances(self, allowance_type, new_amount):
        """
        ενημερωση επιδοματος

        @param allowance_type: 'research', 'library', or 'family'
        @param new_amount: new allowance amount (no decrease allowed)
        @return: True on success, False on failure
        """
        cursor = None
        try:
            amount = float(new_amount)
            if amount <= 0:
                return False

            if allowance_type not in ('research', 'library', 'family'):
                return False

            today = datetime.now().date()

            cursor = self.connection.cursor(dictionary=True)
            self.connection.start_transaction()

            cursor.execute(
                """
                SELECT allowance_id, price, calculation_method, applied_to
                FROM allowances
                WHERE allowance_type = %s
                  AND valid_to IS NULL
                ORDER BY valid_from DESC
                LIMIT 1
                """,
                (allowance_type,),
            )
            row = cursor.fetchone()

            if row:
                current_price = float(row['price'])
                if amount < current_price:
                    self.connection.rollback()
                    return False
                if amount == current_price:
                    self.connection.rollback()
                    return True

                cursor.execute(
                    "UPDATE allowances SET valid_to = %s WHERE allowance_id = %s",
                    (today, row['allowance_id']),
                )
                calculation_method = row['calculation_method']
                applied_to = row['applied_to']
            else:
                defaults = {
                    'family': ('percentage', 'all'),
                    'research': ('fixed', 'permanent_teaching'),
                    'library': ('fixed', 'contract_teaching'),
                }
                calculation_method, applied_to = defaults[allowance_type]

            cursor.execute(
                """
                INSERT INTO allowances (
                    allowance_type,
                    calculation_method,
                    price,
                    applied_to,
                    valid_from,
                    valid_to
                ) VALUES (%s, %s, %s, %s, %s, NULL)
                """,
                (allowance_type, calculation_method, amount, applied_to, today),
            )

            self.connection.commit()
            return True
        except (Error, ValueError, TypeError) as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error updating allowance: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

                
    def terminate_employee(self, employee_id, termination_date):
        """
        απολυση εργαζομενου

        @param employee_id: int - employee id
        @param termination_date: str - YYYY-MM-DD (must be last day of month)
        @return: bool - True on success, False on failure
        """
        cursor = None
        try:
            if not termination_date:
                return False
            term_date = datetime.strptime(termination_date.strip(), "%Y-%m-%d").date()

            next_month = (term_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            last_day = next_month - timedelta(days=1)
            if term_date != last_day:
                return False

            cursor = self.connection.cursor(dictionary=True)
            self.connection.start_transaction()

            cursor.execute(
                "SELECT employee_status, hire_date FROM employees WHERE employee_id = %s",
                (employee_id,)
            )
            emp = cursor.fetchone()
            if not emp:
                self.connection.rollback()
                return False
            if emp.get('employee_status') != 'active':
                self.connection.rollback()
                return False
            hire_date = emp.get('hire_date')
            if hire_date and term_date < hire_date:
                self.connection.rollback()
                return False

            cursor.execute(
                "UPDATE employees SET employee_status = 'terminated', termination_date = %s WHERE employee_id = %s",
                (term_date, employee_id)
            )

            cursor.execute(
                "SELECT employee_id FROM contract_employees WHERE employee_id = %s",
                (employee_id,)
            )
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE contracts SET employee_status = 'terminated' WHERE employee_id = %s AND employee_status = 'active'",
                    (employee_id,)
                )

            self.connection.commit()
            return True
        except (Error, ValueError) as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error terminating employee {employee_id}: {e}")
            return False
        finally:
            if cursor:
                cursor.close()


    def process_payroll(self, month):
        """
        επεξεργασια payroll για συγκεκριμενο μηνα (YYYY-MM).
        επιστρεφει summary dict with total
        """
        cursor = None
        try:
            if not month or len(month.strip()) != 7:
                return {"total_paid": 0, "num_employees": 0, "breakdown_by_category": []}

            month = month.strip()
            try:
                first_day = datetime.strptime(month + "-01", "%Y-%m-%d").date()
            except ValueError:
                return {"total_paid": 0, "num_employees": 0, "breakdown_by_category": []}

            payment_date = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

            cursor = self.connection.cursor(dictionary=True)

            # if payroll already processed for this month, return existing summary
            cursor.execute("SELECT COUNT(*) AS cnt FROM payments WHERE reference_month = %s", (month,))
            if (cursor.fetchone() or {}).get('cnt', 0) > 0:
                cursor.execute(
                    "SELECT SUM(total_amount) AS total_paid, COUNT(DISTINCT employee_id) AS num_employees FROM payments WHERE reference_month = %s",
                    (month,)
                )
                summary = cursor.fetchone() or {}
                total_paid = float(summary.get('total_paid') or 0)
                num_employees = int(summary.get('num_employees') or 0)

                cursor.execute(
                    """
                    SELECT
                      CASE 
                        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
                        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
                        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
                        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
                        ELSE 'unknown'
                      END AS category,
                      SUM(p.total_amount) AS total
                    FROM payments p
                    JOIN employees e ON p.employee_id = e.employee_id
                    LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
                    LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
                    LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
                    LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
                    WHERE p.reference_month = %s
                    GROUP BY category
                    """,
                    (month,)
                )
                breakdown = [
                    {"category": row.get('category'), "total": float(row.get('total') or 0)}
                    for row in cursor.fetchall()
                ]

                return {
                    "total_paid": total_paid,
                    "num_employees": num_employees,
                    "breakdown_by_category": breakdown,
                }

            # load base salaries active for payment date
            cursor.execute(
                """
                SELECT employee_type, category, amount, valid_from
                FROM base_salaries
                WHERE valid_from <= %s
                  AND (valid_to IS NULL OR valid_to >= %s)
                ORDER BY valid_from DESC
                """,
                (payment_date, payment_date)
            )
            base_salary_rows = cursor.fetchall()
            base_salary_map = {}
            for row in base_salary_rows:
                key = f"{row['employee_type']}_{row['category']}"
                if key not in base_salary_map:
                    base_salary_map[key] = float(row['amount'])

            # load allowances active for payment date
            cursor.execute(
                """
                SELECT allowance_type, calculation_method, price, applied_to, valid_from
                FROM allowances
                WHERE valid_from <= %s
                  AND (valid_to IS NULL OR valid_to >= %s)
                ORDER BY valid_from DESC
                """,
                (payment_date, payment_date)
            )
            allowance_rows = cursor.fetchall()
            allowance_map = {}
            for row in allowance_rows:
                key = row['allowance_type']
                if key not in allowance_map:
                    allowance_map[key] = row

            # fetch employees to pay
            # Include: active employees OR terminated during/after this month
            cursor.execute(
                """
                SELECT
                    e.employee_id,
                    e.marital_status,
                    e.num_children,
                    e.hire_date,
                    pe.employee_id AS is_permanent,
                    ce.employee_id AS is_contract,
                    ts.employee_id AS is_teaching,
                    ads.employee_id AS is_admin,
                    c.contract_salary,
                    c.contract_start,
                    c.contract_end
                FROM employees e
                LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
                LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
                LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
                LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
                LEFT JOIN contracts c
                  ON c.employee_id = e.employee_id
                 AND (c.employee_status = 'active' OR (c.employee_status = 'terminated' AND c.contract_end >= %s))
                 AND c.contract_start <= %s
                 AND c.contract_end >= %s
                WHERE (e.employee_status = 'active'
                       OR (e.employee_status = 'terminated' AND e.termination_date >= %s))
                  AND e.hire_date <= %s
                """,
                (first_day, payment_date, first_day, first_day, payment_date)
            )
            employees = cursor.fetchall()

            def full_years(start_date, end_date):
                years = end_date.year - start_date.year
                if (end_date.month, end_date.day) < (start_date.month, start_date.day):
                    years -= 1
                return max(0, years)

            total_paid = 0.0
            num_employees = 0
            breakdown = {}

            self.connection.start_transaction()

            for emp in employees:
                is_permanent = emp.get('is_permanent') is not None
                is_contract = emp.get('is_contract') is not None
                is_teaching = emp.get('is_teaching') is not None
                is_admin = emp.get('is_admin') is not None

                category = None
                if is_permanent and is_teaching:
                    category = 'permanent_teaching'
                elif is_permanent and is_admin:
                    category = 'permanent_admin'
                elif is_contract and is_teaching:
                    category = 'contract_teaching'
                elif is_contract and is_admin:
                    category = 'contract_admin'

                if not category:
                    continue

                base_salary = 0.0
                if category.startswith('permanent'):
                    base_salary = float(base_salary_map.get(category) or 0)
                    if base_salary <= 0:
                        continue
                else:
                    if emp.get('contract_salary') is None:
                        continue
                    base_salary = float(emp['contract_salary'])

                # years increase for permanent only
                years_increase = 0.0
                if category.startswith('permanent') and emp.get('hire_date'):
                    years = full_years(emp['hire_date'], payment_date)
                    if years > 1:
                        years_increase = base_salary * 0.15 * (years - 1)

                # family allowance
                spouse = 1 if emp.get('marital_status') == 'married' else 0
                children = int(emp.get('num_children') or 0)
                dependents = spouse + children

                family_allowance = 0.0
                family_row = allowance_map.get('family')
                if dependents > 0:
                    if family_row:
                        method = (family_row.get('calculation_method') or '').lower()
                        if method in ('percentage', 'percent'):
                            rate = float(family_row.get('price') or 0)
                            family_allowance = base_salary * rate * dependents
                        else:
                            family_allowance = float(family_row.get('price') or 0) * dependents
                    else:
                        family_allowance = base_salary * 0.05 * dependents

                # research allowance (permanent teaching)
                research_allowance = 0.0
                if category == 'permanent_teaching':
                    research_row = allowance_map.get('research')
                    if research_row:
                        method = (research_row.get('calculation_method') or '').lower()
                        if method in ('percentage', 'percent'):
                            research_allowance = base_salary * float(research_row.get('price') or 0)
                        else:
                            research_allowance = float(research_row.get('price') or 0)

                # library allowance (contract teaching)
                library_allowance = 0.0
                if category == 'contract_teaching':
                    library_row = allowance_map.get('library')
                    if library_row:
                        method = (library_row.get('calculation_method') or '').lower()
                        if method in ('percentage', 'percent'):
                            library_allowance = base_salary * float(library_row.get('price') or 0)
                        else:
                            library_allowance = float(library_row.get('price') or 0)

                total_amount = base_salary + years_increase + family_allowance + research_allowance + library_allowance

                # store payment
                cursor.execute(
                    """
                    INSERT INTO payments (
                        employee_id,
                        payment_date,
                        reference_month,
                        base_salary,
                        years_increase,
                        family_allowance,
                        research_allowance,
                        library_allowance,
                        total_amount
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        emp['employee_id'],
                        payment_date,
                        month,
                        float(round(base_salary, 2)),
                        float(round(years_increase, 2)),
                        float(round(family_allowance, 2)),
                        float(round(research_allowance, 2)),
                        float(round(library_allowance, 2)),
                        float(round(total_amount, 2)),
                    )
                )

                total_paid += total_amount
                num_employees += 1
                breakdown[category] = breakdown.get(category, 0.0) + total_amount

            self.connection.commit()

            breakdown_list = [
                {"category": k, "total": float(v)} for k, v in breakdown.items()
            ]

            return {
                "total_paid": float(total_paid),
                "num_employees": int(num_employees),
                "breakdown_by_category": breakdown_list,
            }
        except Error as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            print(f" Error processing payroll: {e}")
            return {"total_paid": 0, "num_employees": 0, "breakdown_by_category": []}
        finally:
            if cursor:
                cursor.close()


    def get_all_employees(self):
        '''
        λιστα με ολους τους υπαλληλους
        
        @return: list of dict - λίστα με όλους τους υπαλλήλους, κάθε dict περιέχει τα βασικά στοιχεία
        '''
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT * FROM employees
                ORDER BY lastname, firstname
            """
            
            cursor.execute(query)
            employees = cursor.fetchall()
            return employees
            
        except Error as e:
            print(f" Error fetching employees: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    

    def get_employee_by_id(self, employee_id):
        '''
        @param employee_id: int - το ID του υπαλλήλου
        @return: dict - όλα τα στοιχεία του υπαλλήλου ή None αν δεν βρεθεί
        '''
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT * FROM employees
                WHERE employee_id = %s
            """
            
            cursor.execute(query, (employee_id,))
            employee = cursor.fetchone()
            return employee
            
        except Error as e:
            print(f" Error fetching employee: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    

    def get_payroll_by_category(self):
        """
        Payroll summary by category for the most recent processed month.
        Uses view_payroll_by_category (BONUS: SQL Views implementation)
        Falls back to direct query if view doesn't exist.

        @return: list of dict [{category, total_amount}]
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            # Use latest processed month
            cursor.execute("SELECT MAX(reference_month) AS ref_month FROM payments")
            row = cursor.fetchone() or {}
            ref_month = row.get('ref_month')
            if not ref_month:
                return []

            # Try VIEW first, fallback to direct query
            try:
                cursor.execute(
                    """
                    SELECT category, total_amount
                    FROM view_payroll_by_category
                    WHERE reference_month = %s
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            except Error:
                # Fallback: direct query without view
                cursor.execute(
                    """
                    SELECT
                      CASE
                        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
                        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
                        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
                        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
                        ELSE 'unknown'
                      END AS category,
                      SUM(p.total_amount) AS total_amount
                    FROM payments p
                    JOIN employees e ON p.employee_id = e.employee_id
                    LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
                    LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
                    LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
                    LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
                    WHERE p.reference_month = %s
                    GROUP BY category
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f" Error fetching payroll by category: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


    def get_salary_stats_by_category(self):
        """
        Max/min/avg salary by category for the most recent processed month.
        Uses view_salary_stats_by_category (BONUS: SQL Views implementation)
        Falls back to direct query if view doesn't exist.

        @return: list of dict [{category, max_salary, min_salary, avg_salary}]
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute("SELECT MAX(reference_month) AS ref_month FROM payments")
            row = cursor.fetchone() or {}
            ref_month = row.get('ref_month')
            if not ref_month:
                return []

            # Try VIEW first, fallback to direct query
            try:
                cursor.execute(
                    """
                    SELECT category, max_salary, min_salary, avg_salary
                    FROM view_salary_stats_by_category
                    WHERE reference_month = %s
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            except Error:
                # Fallback: direct query without view
                cursor.execute(
                    """
                    SELECT
                      CASE
                        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
                        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
                        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
                        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
                        ELSE 'unknown'
                      END AS category,
                      MAX(p.total_amount) AS max_salary,
                      MIN(p.total_amount) AS min_salary,
                      AVG(p.total_amount) AS avg_salary
                    FROM payments p
                    JOIN employees e ON p.employee_id = e.employee_id
                    LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
                    LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
                    LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
                    LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
                    WHERE p.reference_month = %s
                    GROUP BY category
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f" Error fetching salary stats: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


    def get_salary_increases(self, start_date, end_date):
        """
        Average salary increase percentage between two dates (YYYY-MM-DD).

        @return: dict {avg_increase_percentage}
        """
        cursor = None
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end < start:
                return {"avg_increase_percentage": 0}

            cursor = self.connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT reference_month, AVG(total_amount) AS avg_total
                FROM payments
                WHERE payment_date BETWEEN %s AND %s
                GROUP BY reference_month
                ORDER BY reference_month
                """,
                (start, end)
            )
            rows = cursor.fetchall()
            if len(rows) < 2:
                return {"avg_increase_percentage": 0}

            increases = []
            prev = rows[0]['avg_total']
            for row in rows[1:]:
                curr = row['avg_total']
                if prev and prev > 0:
                    increases.append(((curr - prev) / prev) * 100.0)
                prev = curr

            if not increases:
                return {"avg_increase_percentage": 0}

            avg_inc = sum(increases) / len(increases)
            return {"avg_increase_percentage": float(avg_inc)}
        except (Error, ValueError) as e:
            print(f" Error fetching salary increases: {e}")
            return {"avg_increase_percentage": 0}
        finally:
            if cursor:
                cursor.close()


    def get_employee_payroll_history(self, employee_id):
        """
        Payroll history for a specific employee.
        Uses view_employee_payroll_details (BONUS: SQL Views implementation)
        Falls back to direct query if view doesn't exist.

        @return: list of dict [{payment_date, amount, reference_month, base_salary, allowances breakdown}]
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            # Try VIEW first, fallback to direct query
            try:
                cursor.execute(
                    """
                    SELECT
                        payment_date,
                        reference_month,
                        base_salary,
                        years_increase,
                        family_allowance,
                        research_allowance,
                        library_allowance,
                        total_amount AS amount
                    FROM view_employee_payroll_details
                    WHERE employee_id = %s AND payment_date IS NOT NULL
                    ORDER BY payment_date DESC
                    """,
                    (employee_id,)
                )
                results = cursor.fetchall()
            except Error:
                # Fallback: direct query from payments table
                cursor.execute(
                    """
                    SELECT
                        payment_date,
                        reference_month,
                        base_salary,
                        years_increase,
                        family_allowance,
                        research_allowance,
                        library_allowance,
                        total_amount AS amount
                    FROM payments
                    WHERE employee_id = %s
                    ORDER BY payment_date DESC
                    """,
                    (employee_id,)
                )
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f" Error fetching employee payroll history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


    def get_total_payroll_by_category(self):
        """
        Total payroll by category for the most recent processed month.
        Uses view_payroll_by_category (BONUS: SQL Views implementation)
        Falls back to direct query if view doesn't exist.

        @return: list of dict [{category, total}]
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute("SELECT MAX(reference_month) AS ref_month FROM payments")
            row = cursor.fetchone() or {}
            ref_month = row.get('ref_month')
            if not ref_month:
                return []

            # Try VIEW first, fallback to direct query
            try:
                cursor.execute(
                    """
                    SELECT category, total_amount AS total
                    FROM view_payroll_by_category
                    WHERE reference_month = %s
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            except Error:
                # Fallback: direct query without view
                cursor.execute(
                    """
                    SELECT
                      CASE
                        WHEN pe.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'permanent_teaching'
                        WHEN pe.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'permanent_admin'
                        WHEN ce.employee_id IS NOT NULL AND ts.employee_id IS NOT NULL THEN 'contract_teaching'
                        WHEN ce.employee_id IS NOT NULL AND ads.employee_id IS NOT NULL THEN 'contract_admin'
                        ELSE 'unknown'
                      END AS category,
                      SUM(p.total_amount) AS total
                    FROM payments p
                    JOIN employees e ON p.employee_id = e.employee_id
                    LEFT JOIN permanent_employees pe ON pe.employee_id = e.employee_id
                    LEFT JOIN contract_employees ce ON ce.employee_id = e.employee_id
                    LEFT JOIN teaching_staff ts ON ts.employee_id = e.employee_id
                    LEFT JOIN administrative_staff ads ON ads.employee_id = e.employee_id
                    WHERE p.reference_month = %s
                    GROUP BY category
                    ORDER BY category
                    """,
                    (ref_month,)
                )
                results = cursor.fetchall()
            return results
        except Error as e:
            print(f" Error fetching total payroll by category: {e}")
            return []
        finally:
            if cursor:
                cursor.close()


    def execute_custom_query(self, sql_query):
        '''
        εκτέλεση κάποιου custom sql query
        
        @param sql_query: str - Το SQL query προς εκτέλεση
        @return: list of dict - αποτελέσματα του query ή error message
        '''
        cursor = None
        try:
            if not sql_query or not sql_query.strip():
                return []

            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(sql_query)

            if cursor.with_rows:
                results = cursor.fetchall()
            else:
                self.connection.commit()
                results = [{"status": "ok", "rows_affected": cursor.rowcount}]

            return results
        except Error as e:
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.rollback()
            except Error:
                pass
            return [{"error": str(e)}]

        finally:
            if cursor:
                cursor.close()

    def close(self):
        '''
        κλεισιμο συνδεσης
        '''
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(" Connection closed")