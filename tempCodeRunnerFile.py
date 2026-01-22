   def get_departments(self):
        '''
        λιστα με ολα τα τμηματα
        
        @return: list of str - ονόματα τμημάτων
        '''
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT DISTINCT department
                FROM employees
                WHERE employee_status = 'active'
                ORDER BY department
            """
            
            cursor.execute(query)
            departments = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            return departments
            
        except Error as e:
            print(f" Error fetching departments: {e}")
            return []
    