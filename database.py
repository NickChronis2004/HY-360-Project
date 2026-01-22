import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
                database="HY360"
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
            
            cursor.close()
            return departments
            
        except Error as e:
            print(f" Error fetching departments: {e}")
            return []


    def get_active_employees(self):
        '''
        λιστα με ενεργους υπαλληλους (χωρις απολυμενους)
        
        @return: list of dict - μόνο ενεργοί υπάλληλοι
        '''
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    employee_id,
                    firstname,
                    lastname,
                    department_id,
                    d.department_name AS department_name,
                    hire_date,
                    employee_status
                FROM employees e
                JOIN departments d ON e.department_id = d.department_id
                WHERE employee_status = 'active'
                ORDER BY lastname, firstname
            """
            
            cursor.execute(query)
            employees = cursor.fetchall()
            
            cursor.close()
            return employees
            
        except Error as e:
            print(f" Error fetching active employees: {e}")
            return []


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
        # TODO
        pass
    

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
        #TODO
        pass
    

    def update_employee(self, employee_id, data):
        '''
        ενημερωση στοιχειων υπαλληλου
        
        @param employee_id: int - το ID του υπαλλήλου προς ενημέρωση
        @param data: dict με στοιχεία προς αλλαγή (μπορεί να περιέχει οποιοδήποτε από τα πεδία του υπαλλήλου)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        #TODO
        pass
    

    def update_base_salaries(self, category, new_amount):
        '''
        ενημερωση βασικου μισθου
        
        @param category: str - κατηγορία προσωπικού ('permanent_admin', 'permanent_teaching', κλπ)
        @param new_amount: float - νέο ποσό βασικού μισθού (δεν επιτρέπεται μείωση)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        #TODO
        pass
    

    def update_allowances(self, allowance_type, new_amount):
        '''
        μεταβολη επιδοματων
        
        @param allowance_type: str - τύπος επιδόματος ('research', 'library', 'family')
        @param new_amount: float - νέο ποσό επιδόματος (δεν επιτρέπεται μείωση)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        #TODO
        pass
    
    
    def terminate_employee(self, employee_id, termination_date):
        '''
        τερματισμος συμβασης/απολυση
        
        @param employee_id: int - το ID του υπαλλήλου
        @param termination_date: str - ημερομηνία απόλυσης/συνταξιοδότησης (YYYY-MM-DD, μόνο τελευταία μέρα μήνα)
        @return: bool - True αν επιτύχει, False αν αποτύχει
        '''
        #TODO
        pass
    

    def process_payroll(self, month):
        '''
        καταβολη μισθοδοσιας
        
        @param month: str - μήνας για καταβολή (YYYY-MM)
        @return: dict - περιέχει:
            - total_paid: float - συνολικό ποσό που καταβλήθηκε
            - num_employees: int - αριθμός υπαλλήλων που πληρώθηκαν
            - breakdown_by_category: list of dict - ανάλυση ανά κατηγορία
        '''
        #TODO
        pass
    

    def get_all_employees(self):
        '''
        λιστα με ολους τους υπαλληλους
        
        @return: list of dict - λίστα με όλους τους υπαλλήλους, κάθε dict περιέχει τα βασικά στοιχεία
        '''
        #TODO
        pass
    

    def get_employee_by_id(self, employee_id):
        '''
        @param employee_id: int - το ID του υπαλλήλου
        @return: dict - όλα τα στοιχεία του υπαλλήλου ή None αν δεν βρεθεί
        '''
        #TODO
        pass
    

    def get_payroll_by_category(self):
        '''
        κατασταση μισθοδοσιας ανα κατηγορια
        
        @return: list of dict - κάθε dict περιέχει:
            - category: str - κατηγορία προσωπικού
            - total_amount: float - συνολικό ποσό μισθοδοσίας
        '''
        #TODO
        pass
    

    def get_salary_stats_by_category(self):
        '''
        μεγιστος/ελαχιστος/μεσος μισθος ανα κατηγορια
        
        @return: list of dict - κάθε dict περιέχει:
            - category: str - κατηγορία προσωπικού
            - max_salary: float - μέγιστος μισθός
            - min_salary: float - ελάχιστος μισθός
            - avg_salary: float - μέσος μισθός
        '''
        #TODO
        pass
    

    def get_salary_increases(self, start_date, end_date):
        '''
        μεση αυξηση μισθων ανα περιοδο
        
        @param start_date: str - ημερομηνία έναρξης περιόδου (YYYY-MM-DD)
        @param end_date: str - ημερομηνία λήξης περιόδου (YYYY-MM-DD)
        @return: dict - περιέχει:
            - avg_increase_percentage: float - μέση ποσοστιαία αύξηση
        '''
        #TODO
        pass
    

    def get_employee_payroll_history(self, employee_id):
        '''
        ιστορικο μισθοδοσιας υπαλληλου
        
        @param employee_id: int - το ID του υπαλλήλου
        @return: list of dict - κάθε dict περιέχει:
            - payment_date: str - ημερομηνία πληρωμής
            - amount: float - ποσό πληρωμής
        '''
        #TODO
        pass
    

    def get_total_payroll_by_category(self):
        '''
        συνολικο υψος μισθοδοσιας ανα κατηγορια
        
        @return: list of dict - κάθε dict περιέχει:
            - category: str - κατηγορία προσωπικού
            - total: float - συνολικό ύψος μισθοδοσίας
        '''
        #TODO
        pass
    

    def execute_custom_query(self, sql_query):
        '''
        εκτέλεση κάποιου custom sql query
        
        @param sql_query: str - Το SQL query προς εκτέλεση
        @return: list of dict - αποτελέσματα του query ή error message
        '''
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

            cursor.close()
            return results
        except Error as e:
            return [{"error": str(e)}]

    def close(self):
        '''
        κλεισιμο συνδεσης
        '''
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(" Connection closed")