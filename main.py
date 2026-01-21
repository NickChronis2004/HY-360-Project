import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from datetime import datetime

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
        
        # Row 4: Αριθμός παιδιών
        ttk.Label(frame, text="Αριθμός Παιδιών:").grid(row=4, column=0, sticky='w', pady=5)
        children_spin = ttk.Spinbox(frame, from_=0, to=10, width=10)
        children_spin.set(0)
        children_spin.grid(row=4, column=1, sticky='w', pady=5)
        
        # Row 5: Κατηγορία
        ttk.Label(frame, text="Κατηγορία:").grid(row=5, column=0, sticky='w', pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(frame, textvariable=category_var, width=38,
                                     values=["Μόνιμος", "Συμβασιούχος","Διδακτικός", "Διοικητικός"],
                                     state='readonly')
        category_combo.grid(row=5, column=1, pady=5)
        category_combo.current(0)
        
        # Row 6: Τμήμα
        ttk.Label(frame, text="Τμήμα:").grid(row=6, column=0, sticky='w', pady=5)
        dept_entry = ttk.Entry(frame, width=40)
        dept_entry.grid(row=6, column=1, pady=5)
        
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
            if not firstname_entry.get() or not lastname_entry.get() or not category_var.get() or not dept_entry.get():
                messagebox.showerror("Σφάλμα", "Συμπληρώστε όλα τα υποχρεωτικά πεδία")
                return
            
            # Collect data
            data = {
                'firstname': firstname_entry.get(),
                'lastname': lastname_entry.get(),
                'marital_status': marital_var.get(),
                'num_children': int(children_spin.get()),
                'category': category_var.get(),
                'department': dept_entry.get(),
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
        # Παρόμοιο με hire_permanent αλλά με επιπλέον πεδία:
        # - contract_start, contract_end, contract_salary
        messagebox.showinfo("TODO", "Φόρμα σύναψης σύμβασης - όπως η πρόσληψη μόνιμου + 3 πεδία")
    
    # ========== ΑΛΛΑΓΗ ΣΤΟΙΧΕΙΩΝ ==========
    def open_update_employee(self):
        """Παράθυρο αλλαγής στοιχείων"""
        window = tk.Toplevel(self.root)
        window.title("Αλλαγή Στοιχείων Υπαλλήλου")
        window.geometry("600x500")
        
        frame = ttk.Frame(window, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Search section
        ttk.Label(frame, text="Επιλογή Υπαλλήλου", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Employee list
        employees = self.db.get_all_employees()
        
        employee_var = tk.StringVar()
        employee_combo = ttk.Combobox(frame, textvariable=employee_var, width=50)
        employee_combo['values'] = [f"{emp['employee_id']} - {emp['name']}" for emp in employees]
        employee_combo.pack(pady=10)
        
        def load_employee():
            if not employee_var.get():
                return
            
            emp_id = int(employee_var.get().split(' - ')[0])
            emp_data = self.db.get_employee_by_id(emp_id)
            
            # Show edit form with current data
            messagebox.showinfo("TODO", f"Φόρτωσε δεδομένα για: {emp_data['name']}")
        
        ttk.Button(frame, text="Επεξεργασία", command=load_employee).pack(pady=10)
        ttk.Button(frame, text="Κλείσιμο", command=window.destroy).pack(pady=5)
    
    # ========== ΜΕΤΑΒΟΛΗ ΜΙΣΘΩΝ ==========
    def open_salary_adjustment(self):
        """Παράθυρο μεταβολής μισθών/επιδομάτων"""
        messagebox.showinfo("TODO", "Φόρμα μεταβολής μισθών & επιδομάτων")
    
    # ========== ΑΠΟΛΥΣΗ ==========
    def open_termination(self):
        """Παράθυρο απόλυσης/συνταξιοδότησης"""
        messagebox.showinfo("TODO", "Φόρμα απόλυσης/συνταξιοδότησης")
    
    # ========== ΚΑΤΑΒΟΛΗ ΜΙΣΘΟΔΟΣΙΑΣ ==========
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
        # Ask for date range
        messagebox.showinfo("TODO", "Ζήτα ημερομηνίες και δείξε αποτέλεσμα")
    
    def report_employee_details(self):
        """Αναφορά 4"""
        # Ask for employee
        messagebox.showinfo("TODO", "Επιλογή υπαλλήλου και προβολή στοιχείων")
    
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