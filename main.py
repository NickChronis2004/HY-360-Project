import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from datetime import datetime, timedelta

class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Σύστημα Μισθοδοσίας Πανεπιστημίου Κρήτης")
        self.root.geometry("600x700")
        
        # Database connection
        self.db = DatabaseManager()
        
        # Main menu
        self.create_main_menu()
    
    def create_main_menu(self):
        """Κεντρικό μενού με όλες τις λειτουργίες"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title = ttk.Label(main_frame, 
                         text="Σύστημα Μισθοδοσίας\nΠανεπιστημίου Κρήτης",
                         font=('Arial', 18, 'bold'),
                         justify='center')
        title.pack(pady=20)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(expand=True)
        
        # === ΔΙΑΔΙΚΑΣΙΕΣ ===
        ttk.Label(btn_frame, text="Βασικές Διαδικασίες", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0,10), sticky='w')
        
        ttk.Button(btn_frame, text="Πρόσληψη Μόνιμου Υπαλλήλου",
                  command=self.open_hire_permanent, width=40).grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Σύναψη Σύμβασης",
                  command=self.open_hire_contract, width=40).grid(row=2, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Αλλαγή Στοιχείων Υπαλλήλου",
                  command=self.open_update_employee, width=40).grid(row=3, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Μεταβολή Μισθών/Επιδομάτων",
                  command=self.open_salary_adjustment, width=40).grid(row=4, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Απόλυση/Συνταξιοδότηση",
                  command=self.open_termination, width=40).grid(row=5, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Καταβολή Μισθοδοσίας",
                  command=self.open_payroll, width=40).grid(row=6, column=0, pady=5)
        
        # === ΑΝΑΦΟΡΕΣ ===
        ttk.Label(btn_frame, text="Ερωτήσεις & Αναφορές", 
                 font=('Arial', 12, 'bold')).grid(row=7, column=0, pady=(20,10), sticky='w')
        
        ttk.Button(btn_frame, text="Αναφορές & Στατιστικά",
                  command=self.open_reports, width=40).grid(row=8, column=0, pady=5)
        
        # === ΕΞΟΔΟΣ ===
        ttk.Button(btn_frame, text="Έξοδος",
                  command=self.exit_app, width=40).grid(row=9, column=0, pady=20)
    
    # ========== ΠΡΟΣΛΗΨΗ ΜΟΝΙΜΟΥ ==========
    def _get_departments(self):
        """Return department list for dropdowns."""
        return self.db.get_departments()

    def _get_active_employees(self):
        """Return active employees list for dropdowns."""
        return self.db.get_active_employees()

    def open_hire_permanent(self):
        """Παράθυρο πρόσληψης μόνιμου υπαλλήλου"""
        window = tk.Toplevel(self.root)
        window.title("Πρόσληψη Μόνιμου Υπαλλήλου")
        window.geometry("500x750")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Row 0: Τίτλος
        ttk.Label(frame, text="Πρόσληψη Μόνιμου Υπαλλήλου", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Row 1: Όνομα
        ttk.Label(frame, text="Όνομα:").grid(row=1, column=0, sticky='w', pady=5)
        firstname_entry = ttk.Entry(frame, width=40)
        firstname_entry.grid(row=1, column=1, pady=5)
        
        # Row 2: Επώνυμο
        ttk.Label(frame, text="Επώνυμο:").grid(row=2, column=0, sticky='w', pady=5)
        lastname_entry = ttk.Entry(frame, width=40)
        lastname_entry.grid(row=2, column=1, pady=5)

        # Row 3: Οικογενειακή κατάσταση
        ttk.Label(frame, text="Οικογενειακή Κατάσταση:").grid(row=3, column=0, sticky='w', pady=5)
        marital_var = tk.StringVar(value="single")
        marital_frame = ttk.Frame(frame)
        marital_frame.grid(row=3, column=1, sticky='w', pady=5)
        ttk.Radiobutton(marital_frame, text="Άγαμος/η", variable=marital_var, 
                       value="single").pack(side='left', padx=5)
        ttk.Radiobutton(marital_frame, text="Έγγαμος/η", variable=marital_var, 
                       value="married").pack(side='left', padx=5)
        
        # Row 4: Αριθμός ανήλικων παιδιών
        ttk.Label(frame, text="Αριθμός ανήλικων παιδιών:").grid(row=4, column=0, sticky='w', pady=5)
        children_spin = ttk.Spinbox(frame, from_=0, to=10, width=10)
        children_spin.set(0)
        children_spin.grid(row=4, column=1, sticky='w', pady=5)
        
        # Row 5: Κατηγορία
        ttk.Label(frame, text="Κατηγορία:").grid(row=5, column=0, sticky='w', pady=5)
        category_frame = ttk.Frame(frame)
        category_frame.grid(row=5, column=1, sticky='w', pady=5)

        ttk.Label(category_frame, text="Σχέση:").grid(row=0, column=0, sticky='w')
        employment_var = tk.StringVar(value="permanent")
        ttk.Radiobutton(category_frame, text="Μόνιμος", variable=employment_var, value="permanent").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(category_frame, text="Συμβασιούχος", variable=employment_var, value="contract").grid(row=0, column=2, padx=5)

        ttk.Label(category_frame, text="Κλάδος:").grid(row=1, column=0, sticky='w', pady=(5, 0))
        staff_var = tk.StringVar(value="admin")
        ttk.Radiobutton(category_frame, text="Διοικητικός", variable=staff_var, value="admin").grid(row=1, column=1, padx=5, pady=(5, 0))
        ttk.Radiobutton(category_frame, text="Διδακτικός", variable=staff_var, value="teaching").grid(row=1, column=2, padx=5, pady=(5, 0))

        # Row 6: Τμήμα
        ttk.Label(frame, text="Τμήμα:").grid(row=6, column=0, sticky='w', pady=5)
        departments = self._get_departments()
        dept_var = tk.StringVar()
        dept_names = [d["department_name"] for d in departments]
        dept_map = {d["department_name"]: d["department_id"] for d in departments}
        dept_combo = ttk.Combobox(frame, textvariable=dept_var, width=38,
                                  values=dept_names, state='readonly')
        if dept_names:
            dept_combo.current(0)
        dept_combo.grid(row=6, column=1, pady=5)
        
        # Row 7: Ημερομηνία έναρξης
        ttk.Label(frame, text="Ημερομηνία Έναρξης:").grid(row=7, column=0, sticky='w', pady=5)
        hire_date_entry = ttk.Entry(frame, width=40)
        # Υπολογισμός ημερομηνίας (1η του επόμενου μήνα)
        today = datetime.now()
        if today.month == 12:
            next_month = f"{today.year + 1}-01-01"
        else:
            next_month = f"{today.year}-{today.month + 1:02d}-01"
        hire_date_entry.insert(0, next_month)
        hire_date_entry.grid(row=7, column=1, pady=5)
        
        # Row 8: Διεύθυνση
        ttk.Label(frame, text="Διεύθυνση:").grid(row=8, column=0, sticky='w', pady=5)
        address_entry = ttk.Entry(frame, width=40)
        address_entry.grid(row=8, column=1, pady=5)
        
        # Row 9: Τηλέφωνο
        ttk.Label(frame, text="Τηλέφωνο:").grid(row=9, column=0, sticky='w', pady=5)
        phone_entry = ttk.Entry(frame, width=40)
        phone_entry.grid(row=9, column=1, pady=5)
        
        # Row 10: Αριθμός λογαριασμού
        ttk.Label(frame, text="Αρ. Τραπεζικού Λογ/σμού:").grid(row=10, column=0, sticky='w', pady=5)
        bank_acc_entry = ttk.Entry(frame, width=40)
        bank_acc_entry.grid(row=10, column=1, pady=5)
        
        # Row 11: Όνομα τράπεζας
        ttk.Label(frame, text="Όνομα Τράπεζας:").grid(row=11, column=0, sticky='w', pady=5)
        bank_name_entry = ttk.Entry(frame, width=40)
        bank_name_entry.grid(row=11, column=1, pady=5)
        
        # Function Submit
        def submit_hire():
            # Validation
            if not firstname_entry.get() or not lastname_entry.get() or not employment_var.get() or not staff_var.get() or not dept_var.get():
                messagebox.showerror("Σφάλμα", "Συμπληρώστε όλα τα υποχρεωτικά πεδία")
                return

            if employment_var.get() != "permanent":
                messagebox.showerror("Σφάλμα", "Για συμβασιούχο χρησιμοποιήστε τη φόρμα σύναψης σύμβασης")
                return

            # Collect data
            category_code = f"{employment_var.get()}_{staff_var.get()}"
            data = {
                'firstname': firstname_entry.get(),
                'lastname': lastname_entry.get(),
                'marital_status': marital_var.get(),
                'num_children': int(children_spin.get()),
                'category': category_code,
                'department_id': dept_map.get(dept_var.get()),
                'hire_date': hire_date_entry.get(),
                'address': address_entry.get(),
                'phone': phone_entry.get(),
                'bank_account': bank_acc_entry.get(),
                'bank_name': bank_name_entry.get()
            }
            
            # Call DB function
            employee_id = self.db.hire_permanent_employee(data)
            
            if employee_id:
                messagebox.showinfo("Επιτυχία", 
                                   f"Ο υπάλληλος {data['firstname']} {data['lastname']} προστέθηκε με ID: {employee_id}")
                window.destroy()
            else:
                messagebox.showerror("Σφάλμα", "Αποτυχία εισαγωγής")

# Row 12: Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=12, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Υποβολή", command=submit_hire).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ακύρωση", command=window.destroy).pack(side='left', padx=5)
    # ========== ΣΥΝΑΨΗ ΣΥΜΒΑΣΗΣ ==========
    def open_hire_contract(self):
        """Παράθυρο σύναψης σύμβασης"""
        window = tk.Toplevel(self.root)
        window.title("Σύναψη Σύμβασης")
        window.geometry("520x820")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Σύναψη Σύμβασης", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Row 1: Όνομα
        ttk.Label(frame, text="Όνομα:").grid(row=1, column=0, sticky='w', pady=5)
        firstname_entry = ttk.Entry(frame, width=40)
        firstname_entry.grid(row=1, column=1, pady=5)
        
        # Row 2: Επώνυμο
        ttk.Label(frame, text="Επώνυμο:").grid(row=2, column=0, sticky='w', pady=5)
        lastname_entry = ttk.Entry(frame, width=40)
        lastname_entry.grid(row=2, column=1, pady=5)

        # Row 3: Οικογενειακή κατάσταση
        ttk.Label(frame, text="Οικογενειακή Κατάσταση:").grid(row=3, column=0, sticky='w', pady=5)
        marital_var = tk.StringVar(value="single")
        marital_frame = ttk.Frame(frame)
        marital_frame.grid(row=3, column=1, sticky='w', pady=5)
        ttk.Radiobutton(marital_frame, text="Άγαμος/η", variable=marital_var, 
                       value="single").pack(side='left', padx=5)
        ttk.Radiobutton(marital_frame, text="Έγγαμος/η", variable=marital_var, 
                       value="married").pack(side='left', padx=5)
        
        # Row 4: Αριθμός ανήλικων παιδιών
        ttk.Label(frame, text="Αριθμός ανήλικων παιδιών:").grid(row=4, column=0, sticky='w', pady=5)
        children_spin = ttk.Spinbox(frame, from_=0, to=10, width=10)
        children_spin.set(0)
        children_spin.grid(row=4, column=1, sticky='w', pady=5)
        
        # Row 5: Κατηγορία
        ttk.Label(frame, text="Κατηγορία:").grid(row=5, column=0, sticky='w', pady=5)
        category_frame = ttk.Frame(frame)
        category_frame.grid(row=5, column=1, sticky='w', pady=5)

        ttk.Label(category_frame, text="Σχέση:").grid(row=0, column=0, sticky='w')
        employment_var = tk.StringVar(value="contract")
        ttk.Radiobutton(category_frame, text="Μόνιμος", variable=employment_var, value="permanent").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(category_frame, text="Συμβασιούχος", variable=employment_var, value="contract").grid(row=0, column=2, padx=5)

        ttk.Label(category_frame, text="Κλάδος:").grid(row=1, column=0, sticky='w', pady=(5, 0))
        staff_var = tk.StringVar(value="admin")
        ttk.Radiobutton(category_frame, text="Διοικητικός", variable=staff_var, value="admin").grid(row=1, column=1, padx=5, pady=(5, 0))
        ttk.Radiobutton(category_frame, text="Διδακτικός", variable=staff_var, value="teaching").grid(row=1, column=2, padx=5, pady=(5, 0))
        
        # Row 6: Τμήμα
        ttk.Label(frame, text="Τμήμα:").grid(row=6, column=0, sticky='w', pady=5)
        departments = self._get_departments()
        dept_var = tk.StringVar()
        dept_names = [d["department_name"] for d in departments]
        dept_map = {d["department_name"]: d["department_id"] for d in departments}
        dept_combo = ttk.Combobox(frame, textvariable=dept_var, width=38,
                                  values=dept_names, state='readonly')
        if dept_names:
            dept_combo.current(0)
        dept_combo.grid(row=6, column=1, pady=5)
        
        # Row 7: Ημερομηνία έναρξης
        ttk.Label(frame, text="Ημερομηνία Έναρξης:").grid(row=7, column=0, sticky='w', pady=5)
        hire_date_entry = ttk.Entry(frame, width=40)
        today = datetime.now()
        if today.month == 12:
            next_month = f"{today.year + 1}-01-01"
        else:
            next_month = f"{today.year}-{today.month + 1:02d}-01"
        hire_date_entry.insert(0, next_month)
        hire_date_entry.grid(row=7, column=1, pady=5)
        
        # Row 8: Διεύθυνση
        ttk.Label(frame, text="Διεύθυνση:").grid(row=8, column=0, sticky='w', pady=5)
        address_entry = ttk.Entry(frame, width=40)
        address_entry.grid(row=8, column=1, pady=5)
        
        # Row 9: Τηλέφωνο
        ttk.Label(frame, text="Τηλέφωνο:").grid(row=9, column=0, sticky='w', pady=5)
        phone_entry = ttk.Entry(frame, width=40)
        phone_entry.grid(row=9, column=1, pady=5)
        
        # Row 10: Αριθμός λογαριασμού
        ttk.Label(frame, text="Αρ. Τραπεζικού Λογ/σμού:").grid(row=10, column=0, sticky='w', pady=5)
        bank_acc_entry = ttk.Entry(frame, width=40)
        bank_acc_entry.grid(row=10, column=1, pady=5)
        
        # Row 11: Όνομα τράπεζας
        ttk.Label(frame, text="Όνομα Τράπεζας:").grid(row=11, column=0, sticky='w', pady=5)
        bank_name_entry = ttk.Entry(frame, width=40)
        bank_name_entry.grid(row=11, column=1, pady=5)

        # Row 12: Ημερομηνία Έναρξης Σύμβασης
        ttk.Label(frame, text="Έναρξη Σύμβασης (YYYY-MM-DD):").grid(row=12, column=0, sticky='w', pady=5)
        contract_start_entry = ttk.Entry(frame, width=40)
        contract_start_entry.insert(0, next_month)
        contract_start_entry.grid(row=12, column=1, pady=5)

        # Row 13: Ημερομηνία Λήξης Σύμβασης
        ttk.Label(frame, text="Λήξη Σύμβασης (YYYY-MM-DD):").grid(row=13, column=0, sticky='w', pady=5)
        contract_end_entry = ttk.Entry(frame, width=40)
        contract_end_entry.grid(row=13, column=1, pady=5)

        # Row 14: Μισθός Σύμβασης
        ttk.Label(frame, text="Μισθός Σύμβασης:").grid(row=14, column=0, sticky='w', pady=5)
        contract_salary_entry = ttk.Entry(frame, width=40)
        contract_salary_entry.grid(row=14, column=1, pady=5)

        def parse_date(value):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return None

        def submit_contract():
            if not firstname_entry.get() or not lastname_entry.get() or not dept_var.get():
                messagebox.showerror("Σφάλμα", "Συμπληρώστε όλα τα υποχρεωτικά πεδία")
                return

            if employment_var.get() != "contract":
                messagebox.showerror("Σφάλμα", "Για μόνιμο υπάλληλο χρησιμοποιήστε την φόρμα πρόσληψης μόνιμου")
                return

            hire_date = parse_date(hire_date_entry.get())
            contract_start = parse_date(contract_start_entry.get())
            contract_end = parse_date(contract_end_entry.get())
            if not hire_date or not contract_start or not contract_end:
                messagebox.showerror("Σφάλμα", "Λάθος μορφή ημερομηνίας. Χρησιμοποιήστε YYYY-MM-DD")
                return

            if hire_date.day != 1 or contract_start.day != 1:
                messagebox.showerror("Σφάλμα", "Η ημερομηνία έναρξης πρέπει να είναι 1η του μήνα")
                return

            if contract_end < contract_start:
                messagebox.showerror("Σφάλμα", "Η λήξη σύμβασης πρέπει να είναι μετά την έναρξη")
                return

            try:
                contract_salary = float(contract_salary_entry.get())
            except ValueError:
                messagebox.showerror("Σφάλμα", "Ο μισθός σύμβασης πρέπει να είναι αριθμός")
                return

            category_code = f"{employment_var.get()}_{staff_var.get()}"
            data = {
                'firstname': firstname_entry.get(),
                'lastname': lastname_entry.get(),
                'marital_status': marital_var.get(),
                'num_children': int(children_spin.get()),
                'category': category_code,
                'department_id': dept_map.get(dept_var.get()),
                'hire_date': hire_date_entry.get(),
                'address': address_entry.get(),
                'phone': phone_entry.get(),
                'bank_account': bank_acc_entry.get(),
                'bank_name': bank_name_entry.get(),
                'contract_start': contract_start_entry.get(),
                'contract_end': contract_end_entry.get(),
                'contract_salary': contract_salary
            }

            employee_id = self.db.hire_contract_employee(data)

            if employee_id:
                messagebox.showinfo("Επιτυχία", 
                                   f"Ο υπάλληλος {data['firstname']} {data['lastname']} προστέθηκε με ID: {employee_id}")
                window.destroy()
            else:
                messagebox.showerror("Σφάλμα", "Αποτυχία εισαγωγής")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=15, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Υποβολή", command=submit_contract).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ακύρωση", command=window.destroy).pack(side='left', padx=5)

    # ========== ΑΛΛΑΓΗ ΣΤΟΙΧΕΙΩΝ ==========

    def open_update_employee(self):
            """Παράθυρο αλλαγής στοιχείων"""
            window = tk.Toplevel(self.root)
            window.title("Αλλαγή Στοιχείων Υπαλλήλου")
            window.geometry("600x500")
        
            frame = ttk.Frame(window, padding="20")
            frame.pack(fill='both', expand=True)
        
            ttk.Label(frame, text="Επιλογή Υπαλλήλου", 
                     font=('Arial', 12, 'bold')).pack(pady=10)
        
            employees = self._get_active_employees()
            employee_var = tk.StringVar()
            employee_combo = ttk.Combobox(frame, textvariable=employee_var, width=50, state='readonly')
            employee_combo['values'] = [
                f"{emp['employee_id']} - {emp['lastname']} {emp['firstname']}" for emp in employees
            ]
            employee_combo.pack(pady=10)

            def load_employee():
                if not employee_var.get():
                    return
                emp_id = int(employee_var.get().split(' - ')[0])
                emp_data = self.db.get_employee_by_id(emp_id)
                if not emp_data:
                    # Fallback to list data if full fetch not available
                    emp_data = next((emp for emp in employees if emp['employee_id'] == emp_id), {})

                edit_win = tk.Toplevel(window)
                edit_win.title("Επεξεργασία Στοιχείων")
                edit_win.geometry("600x520")

                edit_frame = ttk.Frame(edit_win, padding="20")
                edit_frame.pack(fill='both', expand=True)

                ttk.Label(edit_frame, text=f"Υπάλληλος: {emp_data.get('lastname', '')} {emp_data.get('firstname', '')}",
                         font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

                # Marital status
                ttk.Label(edit_frame, text="Οικογενειακή Κατάσταση:").grid(row=1, column=0, sticky='w', pady=5)
                marital_var = tk.StringVar(value=emp_data.get('marital_status', 'single'))
                marital_frame = ttk.Frame(edit_frame)
                marital_frame.grid(row=1, column=1, sticky='w', pady=5)
                ttk.Radiobutton(marital_frame, text="Άγαμος/η", variable=marital_var, value="single").pack(side='left', padx=5)
                ttk.Radiobutton(marital_frame, text="Έγγαμος/η", variable=marital_var, value="married").pack(side='left', padx=5)

                # Children
                ttk.Label(edit_frame, text="Αριθμός ανήλικων παιδιών:").grid(row=2, column=0, sticky='w', pady=5)
                children_spin = ttk.Spinbox(edit_frame, from_=0, to=10, width=10)
                children_spin.set(emp_data.get('num_children', 0))
                children_spin.grid(row=2, column=1, sticky='w', pady=5)

                # Department (ΔΙΟΡΘΩΣΗ ΕΔΩ)
                ttk.Label(edit_frame, text="Τμήμα:").grid(row=3, column=0, sticky='w', pady=5)
                departments = self._get_departments()
                dept_var = tk.StringVar()
                dept_names = [d["department_name"] for d in departments]
                dept_map = {d["department_name"]: d["department_id"] for d in departments}
                
                dept_combo = ttk.Combobox(edit_frame, textvariable=dept_var, width=40,
                                          values=dept_names, state='readonly')
                
                # --- FIX START ---
                # Βρίσκουμε το όνομα του τμήματος βάσει του department_id του υπαλλήλου
                current_dept_id = emp_data.get('department_id')
                current_dept_name = None
                
                # Ψάχνουμε στη λίστα departments ποιο όνομα αντιστοιχεί στο ID
                for dept in departments:
                    if dept['department_id'] == current_dept_id:
                        current_dept_name = dept['department_name']
                        break
                
                if current_dept_name and current_dept_name in dept_names:
                    dept_combo.set(current_dept_name)
                elif dept_names:
                    dept_combo.current(0)
                # --- FIX END ---
                
                dept_combo.grid(row=3, column=1, pady=5)

                # Address
                ttk.Label(edit_frame, text="Διεύθυνση:").grid(row=4, column=0, sticky='w', pady=5)
                address_entry = ttk.Entry(edit_frame, width=40)
                address_entry.insert(0, emp_data.get('address', '') or '')
                address_entry.grid(row=4, column=1, pady=5)

                # Phone
                ttk.Label(edit_frame, text="Τηλέφωνο:").grid(row=5, column=0, sticky='w', pady=5)
                phone_entry = ttk.Entry(edit_frame, width=40)
                phone_entry.insert(0, emp_data.get('phone', '') or '')
                phone_entry.grid(row=5, column=1, pady=5)

                # Bank account
                ttk.Label(edit_frame, text="Αρ. Τραπεζικού Λογ/σμού:").grid(row=6, column=0, sticky='w', pady=5)
                bank_acc_entry = ttk.Entry(edit_frame, width=40)
                bank_acc_entry.insert(0, emp_data.get('bank_account', '') or '')
                bank_acc_entry.grid(row=6, column=1, pady=5)

                # Bank name
                ttk.Label(edit_frame, text="Όνομα Τράπεζας:").grid(row=7, column=0, sticky='w', pady=5)
                bank_name_entry = ttk.Entry(edit_frame, width=40)
                bank_name_entry.insert(0, emp_data.get('bank_name', '') or '')
                bank_name_entry.grid(row=7, column=1, pady=5)

                # Status
                ttk.Label(edit_frame, text="Κατάσταση:").grid(row=8, column=0, sticky='w', pady=5)
                status_var = tk.StringVar(value=emp_data.get('employee_status', 'active'))
                status_combo = ttk.Combobox(edit_frame, textvariable=status_var, width=18,
                                            values=["active", "terminated"], state='readonly')
                status_combo.grid(row=8, column=1, sticky='w', pady=5)

                def submit_update():
                    data = {}

                    if marital_var.get() != emp_data.get('marital_status'):
                        data['marital_status'] = marital_var.get()

                    try:
                        new_children = int(children_spin.get())
                        if new_children != emp_data.get('num_children'):
                            data['num_children'] = new_children
                    except ValueError:
                        messagebox.showerror("Σφάλμα", "Ο αριθμός παιδιών πρέπει να είναι αριθμός")
                        return

                    new_dept_id = dept_map.get(dept_var.get())
                    if new_dept_id and new_dept_id != emp_data.get('department_id'):
                        data['department_id'] = new_dept_id

                    if address_entry.get().strip() and address_entry.get().strip() != (emp_data.get('address') or ''):
                        data['address'] = address_entry.get().strip()

                    if phone_entry.get().strip() and phone_entry.get().strip() != (emp_data.get('phone') or ''):
                        data['phone'] = phone_entry.get().strip()

                    if bank_acc_entry.get().strip() and bank_acc_entry.get().strip() != (emp_data.get('bank_account') or ''):
                        data['bank_account'] = bank_acc_entry.get().strip()

                    if bank_name_entry.get().strip() and bank_name_entry.get().strip() != (emp_data.get('bank_name') or ''):
                        data['bank_name'] = bank_name_entry.get().strip()

                    if status_var.get() and status_var.get() != emp_data.get('employee_status'):
                        data['employee_status'] = status_var.get()

                    if not data:
                        messagebox.showinfo("Πληροφορία", "Δεν υπάρχουν αλλαγές")
                        return

                    success = self.db.update_employee(emp_id, data)
                    if success:
                        messagebox.showinfo("Επιτυχία", "Τα στοιχεία ενημερώθηκαν")
                        edit_win.destroy()
                    else:
                        messagebox.showerror("Σφάλμα", "Αποτυχία ενημέρωσης")

                btn_frame = ttk.Frame(edit_frame)
                btn_frame.grid(row=9, column=0, columnspan=2, pady=15)
                ttk.Button(btn_frame, text="Αποθήκευση", command=submit_update).pack(side='left', padx=5)
                ttk.Button(btn_frame, text="Ακύρωση", command=edit_win.destroy).pack(side='left', padx=5)

            ttk.Button(frame, text="Επεξεργασία", command=load_employee).pack(pady=10)
            ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack(pady=5)
    
        # ========== ΜΕΤΑΒΟΛΗ ΜΙΣΘΩΝ ==========
    def open_salary_adjustment(self):
            """Παράθυρο μεταβολής μισθών/επιδόματων"""
            window = tk.Toplevel(self.root)
            window.title("Μεταβολή Μισθών & Επιδόματων")
            window.geometry("520x420")

            frame = ttk.Frame(window, padding="20")
            frame.pack(fill='both', expand=True)

            ttk.Label(frame, text="Μεταβολή Μισθών & Επιδόματων",
                     font=('Arial', 12, 'bold')).pack(pady=10)

            type_var = tk.StringVar(value="base")

            type_frame = ttk.Frame(frame)
            type_frame.pack(pady=5, fill='x')
            ttk.Radiobutton(type_frame, text="Βασικός Μισθός", variable=type_var, value="base").pack(side='left', padx=5)
            ttk.Radiobutton(type_frame, text="Επίδομα", variable=type_var, value="allowance").pack(side='left', padx=5)

            base_frame = ttk.Frame(frame)
            base_frame.pack(pady=10, fill='x')

            ttk.Label(base_frame, text="Σχέση:").grid(row=0, column=0, sticky='w')
            employment_var = tk.StringVar(value="permanent")
            ttk.Radiobutton(base_frame, text="Μόνιμος", variable=employment_var, value="permanent").grid(row=0, column=1, padx=5)
            ttk.Radiobutton(base_frame, text="Συμβασιούχος", variable=employment_var, value="contract").grid(row=0, column=2, padx=5)

            ttk.Label(base_frame, text="Κλάδος:").grid(row=1, column=0, sticky='w', pady=(5, 0))
            staff_var = tk.StringVar(value="admin")
            ttk.Radiobutton(base_frame, text="Διοικητικός", variable=staff_var, value="admin").grid(row=1, column=1, padx=5, pady=(5, 0))
            ttk.Radiobutton(base_frame, text="Διδακτικός", variable=staff_var, value="teaching").grid(row=1, column=2, padx=5, pady=(5, 0))

            allowance_frame = ttk.Frame(frame)
            allowance_frame.pack(pady=10, fill='x')

            ttk.Label(allowance_frame, text="Επίδομα:").grid(row=0, column=0, sticky='w')
            allowance_display = ["Οικογενειακό", "Έρευνας", "Βιβλιοθήκης"]
            allowance_map = {
                "Οικογενειακό": "family",
                "Έρευνας": "research",
                "Βιβλιοθήκης": "library"
            }
            allowance_var = tk.StringVar(value=allowance_display[0])
            allowance_combo = ttk.Combobox(allowance_frame, textvariable=allowance_var, width=20,
                                           values=allowance_display, state='readonly')
            allowance_combo.grid(row=0, column=1, padx=5)

            # Amount
            ttk.Label(frame, text="Νέο ποσό:").pack(pady=(10, 0))
            amount_entry = ttk.Entry(frame, width=20)
            amount_entry.pack(pady=5)

            def toggle_frames():
                if type_var.get() == "base":
                    base_frame.pack(pady=10, fill='x')
                    allowance_frame.pack_forget()
                else:
                    allowance_frame.pack(pady=10, fill='x')
                    base_frame.pack_forget()

            toggle_frames()
            type_var.trace_add('write', lambda *_: toggle_frames())

            def submit_change():
                try:
                    amount = float(amount_entry.get())
                    if amount <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Σφάλμα", "Το ποσό πρέπει να είναι θετικός αριθμός")
                    return

                if type_var.get() == "base":
                    category_code = f"{employment_var.get()}_{staff_var.get()}"
                    success = self.db.update_base_salaries(category_code, amount)
                else:
                    allowance_type = allowance_map.get(allowance_var.get())
                    success = self.db.update_allowances(allowance_type, amount)

                if success:
                    messagebox.showinfo("Επιτυχία", "Η αλλαγή καταχωρήθηκε")
                    window.destroy()
                else:
                    messagebox.showerror("Σφάλμα", "Αποτυχία ενημέρωσης")

            ttk.Button(frame, text="Υποβολή", command=submit_change).pack(pady=10)
            ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack()
    
        # ========== ΑΠΟΛΥΣΗ ==========
    def open_termination(self):
            """Termination/retirement window"""
            window = tk.Toplevel(self.root)
            window.title("Απόλυση/Συνταξιοδότηση")
            window.geometry("500x350")

            frame = ttk.Frame(window, padding="20")
            frame.pack(fill='both', expand=True)

            ttk.Label(frame, text="Επιλογή Υπαλλήλου",
                     font=('Arial', 12, 'bold')).pack(pady=10)

            employees = self._get_active_employees()
            employee_var = tk.StringVar()
            employee_combo = ttk.Combobox(frame, textvariable=employee_var, width=50, state='readonly')
            employee_combo['values'] = [
                f"{emp['employee_id']} - {emp['lastname']} {emp['firstname']}" for emp in employees
            ]
            employee_combo.pack(pady=10)

            ttk.Label(frame, text="Ημερομηνία Τερματισμού (YYYY-MM-DD):").pack(pady=(10, 0))
            termination_entry = ttk.Entry(frame, width=30)
            termination_entry.pack(pady=5)

            def is_last_day(date_obj):
                next_month = (date_obj.replace(day=28) + timedelta(days=4)).replace(day=1)
                last_day = next_month - timedelta(days=1)
                return date_obj == last_day

            def submit_termination():
                if not employee_var.get() or not termination_entry.get():
                    messagebox.showerror("Σφάλμα", "Συμπληρώστε όλα τα υποχρεωτικά πεδία")
                    return

                try:
                    term_date = datetime.strptime(termination_entry.get(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Σφάλμα", "Λάθος μορφή ημερομηνίας. Χρησιμοποιήστε YYYY-MM-DD")
                    return

                if not is_last_day(term_date):
                    messagebox.showerror("Σφάλμα", "Η απόλυση/συνταξιοδότηση πρέπει να είναι την τελευταία ημέρα του μήνα")
                    return

                emp_id = int(employee_var.get().split(' - ')[0])
                success = self.db.terminate_employee(emp_id, termination_entry.get())

                if success:
                    messagebox.showinfo("Επιτυχία", "Ο υπάλληλος τερματίστηκε")
                    window.destroy()
                else:
                    messagebox.showerror("Σφάλμα", "Αποτυχία τερματισμού")

            ttk.Button(frame, text="Υποβολή", command=submit_termination).pack(pady=10)
            ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack()

    def open_payroll(self):
        """Παράθυρο καταβολής μισθοδοσίας"""
        window = tk.Toplevel(self.root)
        window.title("Καταβολή Μισθοδοσίας")
        window.geometry("500x400")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Καταβολή Μισθοδοσίας", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Month selection
        ttk.Label(frame, text="Επιλέξτε Μήνα:").pack(pady=5)
        month_entry = ttk.Entry(frame, width=20)
        month_entry.insert(0, datetime.now().strftime("%Y-%m"))
        month_entry.pack(pady=5)
        
        result_text = tk.Text(frame, height=15, width=60)
        result_text.pack(pady=10)
        
        def process():
            month = month_entry.get()
            result = self.db.process_payroll(month)
            
            # Display results
            result_text.delete('1.0', tk.END)
            result_text.insert('1.0', f"Καταβολή Μισθοδοσίας - {month}\n")
            result_text.insert(tk.END, "="*50 + "\n\n")
            result_text.insert(tk.END, f"Συνολικό ποσό: {result['total_paid']}€\n")
            result_text.insert(tk.END, f"Αριθμός υπαλλήλων: {result['num_employees']}\n\n")
            result_text.insert(tk.END, "Ανάλυση ανά κατηγορία:\n")
            for cat in result['breakdown_by_category']:
                result_text.insert(tk.END, f"  {cat['category']}: {cat['total']}€\n")
        
        ttk.Button(frame, text="Εκτέλεση Πληρωμής", command=process).pack(pady=10)
        ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack()
    
    # ========== ΑΝΑΦΟΡΕΣ ==========
    def open_reports(self):
        """Παράθυρο αναφορών & ερωτήσεων"""
        window = tk.Toplevel(self.root)
        window.title("Ερωτήσεις & Αναφορές")
        window.geometry("600x500")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Προκαθορισμένες Ερωτήσεις", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Button(frame, text="1. Κατάσταση μισθοδοσίας ανά κατηγορία",
                  command=self.report_payroll_by_category, width=50).pack(pady=5)
        
        ttk.Button(frame, text="2. Μέγιστος/Ελάχιστος/Μέσος μισθός ανά κατηγορία",
                  command=self.report_salary_stats, width=50).pack(pady=5)
        
        ttk.Button(frame, text="3. Μέση αύξηση μισθών ανά περίοδο",
                  command=self.report_salary_increases, width=50).pack(pady=5)
        
        ttk.Button(frame, text="4. Στοιχεία συγκεκριμένου υπαλλήλου",
                  command=self.report_employee_details, width=50).pack(pady=5)
        
        ttk.Button(frame, text="5. Συνολικό ύψος μισθοδοσίας ανά κατηγορία",
                  command=self.report_total_by_category, width=50).pack(pady=5)
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20)
        
        ttk.Label(frame, text="Custom SQL Query", 
                 font=('Arial', 12, 'bold')).pack(pady=5)
        
        ttk.Button(frame, text="Εκτέλεση Custom Query",
                  command=self.custom_query, width=50).pack(pady=5)
    
    def report_payroll_by_category(self):
        """Αναφορά 1"""
        results = self.db.get_payroll_by_category()
        self.show_table_results("Κατάσταση Μισθοδοσίας ανά Κατηγορία", results)
    
    def report_salary_stats(self):
        """Αναφορά 2"""
        results = self.db.get_salary_stats_by_category()
        self.show_table_results("Στατιστικά Μισθών", results)
    
    def report_salary_increases(self):
        """Αναφορά 3"""
        window = tk.Toplevel(self.root)
        window.title("Μέση αύξηση μισθών")
        window.geometry("500x300")

        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Περίοδος", font=('Arial', 12, 'bold')).pack(pady=10)

        ttk.Label(frame, text="Από (YYYY-MM-DD):").pack()
        start_entry = ttk.Entry(frame, width=20)
        start_entry.pack(pady=5)

        ttk.Label(frame, text="Έως (YYYY-MM-DD):").pack()
        end_entry = ttk.Entry(frame, width=20)
        end_entry.pack(pady=5)

        result_label = ttk.Label(frame, text="")
        result_label.pack(pady=10)

        def submit():
            start = start_entry.get().strip()
            end = end_entry.get().strip()
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d").date()
                end_date = datetime.strptime(end, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Σφάλμα", "Λάθος μορφή ημερομηνίας")
                return

            if end_date < start_date:
                messagebox.showerror("Σφάλμα", "Η ημερομηνία λήξης πρέπει να είναι μετά την έναρξη")
                return

            result = self.db.get_salary_increases(start, end)
            if not result:
                result_label.config(text="Δεν βρέθηκαν δεδομένα")
                return

            if isinstance(result, dict) and 'avg_increase_percentage' in result:
                result_label.config(text=f"Μέση αύξηση: {result['avg_increase_percentage']}%")
            else:
                result_label.config(text=str(result))

        ttk.Button(frame, text="Υπολογισμός", command=submit).pack(pady=10)
        ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack()

    def report_employee_details(self):
        """Report 4"""
        window = tk.Toplevel(self.root)
        window.title("Στοιχεία υπαλλήλου")
        window.geometry("600x450")

        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Επιλογή Υπαλλήλου",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        employees = self._get_active_employees()
        employee_var = tk.StringVar()
        employee_combo = ttk.Combobox(frame, textvariable=employee_var, width=50, state='readonly')
        employee_combo['values'] = [
            f"{emp['employee_id']} - {emp['lastname']} {emp['firstname']}" for emp in employees
        ]
        employee_combo.pack(pady=10)

        result_text = tk.Text(frame, height=14, width=70)
        result_text.pack(pady=10)

        def show_details():
            if not employee_var.get():
                return
            emp_id = int(employee_var.get().split(' - ')[0])
            emp_data = next((emp for emp in employees if emp['employee_id'] == emp_id), None)
            if not emp_data:
                messagebox.showerror("Σφάλμα", "Δεν βρέθηκε υπάλληλος")
                return

            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, f"ID: {emp_data['employee_id']}\n")
            result_text.insert(tk.END, f"Name: {emp_data['lastname']} {emp_data['firstname']}\n")
            result_text.insert(tk.END, f"Department: {emp_data['department_name']}\n")
            result_text.insert(tk.END, f"Hire date: {emp_data['hire_date']}\n")
            result_text.insert(tk.END, f"Status: {emp_data['employee_status']}\n\n")

            history = self.db.get_employee_payroll_history(emp_id)
            result_text.insert(tk.END, "Ιστορικό μισθοδοσίας:\n")
            if not history:
                result_text.insert(tk.END, "(δεν υπάρχουν δεδομένα)\n")
            else:
                for row in history:
                    if isinstance(row, dict):
                        date = row.get('payment_date', '')
                        amount = row.get('amount', row.get('total_amount', ''))
                        result_text.insert(tk.END, f"- {date}: {amount}\n")
                    else:
                        result_text.insert(tk.END, f"- {row}\n")

        ttk.Button(frame, text="Προβολή", command=show_details).pack(pady=5)
        ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack()

    def report_total_by_category(self):
            """Αναφορά 5"""
            results = self.db.get_total_payroll_by_category()
            self.show_table_results("Συνολικό Ύψος Μισθοδοσίας", results)
    
    def custom_query(self):
        """Custom SQL Query"""
        window = tk.Toplevel(self.root)
        window.title("Custom SQL Query")
        window.geometry("700x600")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Εισάγετε SQL Query:").pack(pady=5)
        
        query_text = tk.Text(frame, height=5, width=80)
        query_text.pack(pady=5)
        
        result_text = tk.Text(frame, height=20, width=80)
        result_text.pack(pady=10)
        
        def execute():
            query = query_text.get('1.0', tk.END).strip()
            results = self.db.execute_custom_query(query)
            
            result_text.delete('1.0', tk.END)
            for row in results:
                result_text.insert(tk.END, str(row) + "\n")
        
        ttk.Button(frame, text="Εκτέλεση", command=execute).pack(pady=5)
    
    def show_table_results(self, title, data):
        """Εμφάνιση αποτελεσμάτων σε πίνακα"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("700x400")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        if not data:
            ttk.Label(frame, text="Δεν βρέθηκαν αποτελέσματα").pack()
            return
        
        # Create treeview
        columns = list(data[0].keys())
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for row in data:
            tree.insert('', 'end', values=list(row.values()))
        
        tree.pack(fill='both', expand=True)
        
        ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack(pady=10)
    
    # ========== ΕΧΙΤ ==========
    def exit_app(self):
        """Έξοδος από την εφαρμογή"""
        if messagebox.askyesno("Έξοδος", "Είστε σίγουροι ότι θέλετε να κλείσετε την εφαρμογή;"):
            self.db.close()
            self.root.quit()


# ========== MAIN ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()