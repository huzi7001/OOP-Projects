import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageTk
import mysql.connector
from mysql.connector import Error


# ---------------- Database Manager Class ----------------
class DatabaseManager:
    """Handles all database operations."""
    
    def __init__(self):
        self.connection = None
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"  # Change this to your MySQL password
        self.database = "employee_management"
    
    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")
            return False
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE queries."""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            messagebox.showerror("Database Error", f"Query failed:\n{e}")
            return False
    
    def fetch_all(self, query, params=None):
        """Execute SELECT query and return all results."""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            messagebox.showerror("Database Error", f"Failed to fetch data:\n{e}")
            return []
    
    def fetch_one(self, query, params=None):
        """Execute SELECT query and return one result."""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
    
    # --- Employee CRUD Operations ---
    
    def add_employee(self, emp_id, name, base_salary, emp_type, bonus):
        """Insert a new employee into the database."""
        query = """
            INSERT INTO employees (emp_id, name, base_salary, emp_type, bonus)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (emp_id, name, base_salary, emp_type, bonus)
        return self.execute_query(query, params)
    
    def get_all_employees(self):
        """Retrieve all employees from the database."""
        query = "SELECT emp_id, name, base_salary, emp_type, bonus FROM employees ORDER BY emp_id"
        return self.fetch_all(query)
    
    def get_employee_by_id(self, emp_id):
        """Retrieve a single employee by ID."""
        query = "SELECT emp_id, name, base_salary, emp_type, bonus FROM employees WHERE emp_id = %s"
        return self.fetch_one(query, (emp_id,))
    
    def update_employee(self, emp_id, name, base_salary, emp_type, bonus):
        """Update an existing employee."""
        query = """
            UPDATE employees 
            SET name = %s, base_salary = %s, emp_type = %s, bonus = %s
            WHERE emp_id = %s
        """
        params = (name, base_salary, emp_type, bonus, emp_id)
        return self.execute_query(query, params)
    
    def delete_employee(self, emp_id):
        """Delete an employee from the database."""
        query = "DELETE FROM employees WHERE emp_id = %s"
        return self.execute_query(query, (emp_id,))
    
    def employee_exists(self, emp_id):
        """Check if an employee ID already exists."""
        query = "SELECT COUNT(*) FROM employees WHERE emp_id = %s"
        result = self.fetch_one(query, (emp_id,))
        return result[0] > 0 if result else False
    
    def get_employee_count(self):
        """Get total number of employees."""
        query = "SELECT COUNT(*) FROM employees"
        result = self.fetch_one(query)
        return result[0] if result else 0
    
    def search_employees(self, search_term):
        """Search employees by name or ID."""
        query = """
            SELECT emp_id, name, base_salary, emp_type, bonus 
            FROM employees 
            WHERE name LIKE %s OR emp_id LIKE %s
        """
        search_pattern = f"%{search_term}%"
        return self.fetch_all(query, (search_pattern, search_pattern))


# ---------------- Salary Class (Composition) ----------------
class Salary:
    def __init__(self, base_salary):
        self.__base_salary = base_salary

    def get_salary(self):
        return self.__base_salary

    def set_salary(self, new_salary):
        if new_salary > 0:
            self.__base_salary = new_salary
        else:
            print("Invalid Salary!")


# ---------------- Abstract Employee Class ----------------
class Employee(ABC):
    def __init__(self, name, emp_id, salary: Salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    @abstractmethod
    def calculate_bonus(self):
        pass

    def get_info(self):
        return (
            self.name,
            self.emp_id,
            f"${self.salary.get_salary():,.2f}",
            f"${self.calculate_bonus():,.2f}",
            self.__class__.__name__
        )
    
    def get_raw_info(self):
        """Return raw data without formatting for database storage."""
        return (
            self.emp_id,
            self.name,
            self.salary.get_salary(),
            self.__class__.__name__,
            self.calculate_bonus()
        )


# ---------------- Employee Types ----------------
class Manager(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.20


class Developer(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.10


class HR(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.15


class SoftwareEngineer(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.12


class Analyst(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.08


class Designer(Employee):
    def __init__(self, name, emp_id, base_salary):
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.11


# ---------------- Employee Management System (Enhanced GUI with MySQL) ----------------
class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1000x650")
        self.root.configure(bg="#306ca7")
        
        # Initialize database
        self.db = DatabaseManager()
        self.db_connected = self.db.connect()
        
        # Employee type to class mapping
        self.employee_classes = {
            "Manager": Manager,
            "Developer": Developer,
            "HR": HR,
            "Software Engineer": SoftwareEngineer,
            "Analyst": Analyst,
            "Designer": Designer
        }
        
        # Bonus rates for each type
        self.bonus_rates = {
            "Manager": 0.20,
            "Developer": 0.10,
            "HR": 0.15,
            "Software Engineer": 0.12,
            "Analyst": 0.08,
            "Designer": 0.11
        }
        
        self.create_ui()
        
        # Load existing employees from database
        if self.db_connected:
            self.display_all()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_placeholder_image(self):
        """Create a simple placeholder image for the header."""
        try:
            width, height = 60, 60
            img = Image.new('RGB', (width, height), color="#3E2D9B")
            draw = ImageDraw.Draw(img)
            draw.ellipse([18, 12, 42, 36], fill='white', outline='white')
            draw.ellipse([12, 33, 48, 57], fill='white', outline='white')
            return ImageTk.PhotoImage(img)
        except:
            return None

    def create_ui(self):
        """Create enhanced UI components."""
        
        # --- Header Frame ---
        header_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_container = tk.Frame(header_frame, bg="#2196F3")
        title_container.pack(expand=True)
        
        try:
            icon_image = self.create_placeholder_image()
            if icon_image:
                icon_label = tk.Label(title_container, image=icon_image, bg="#22283C")
                icon_label.image = icon_image
                icon_label.pack(side=tk.LEFT, padx=10)
        except:
            pass
        
        title = tk.Label(
            title_container, 
            text="EMPLOYEE MANAGEMENT SYSTEM", 
            font=("Segoe UI", 28, "bold"),
            bg="#2196F3",
            fg="black"
        )
        title.pack(side=tk.LEFT, padx=10)
        
        # Database connection indicator
        db_status = "🟢 Connected" if self.db_connected else "🔴 Disconnected"
        db_label = tk.Label(
            title_container,
            text=db_status,
            font=("Segoe UI", 10),
            bg="#2196F3",
            fg="white"
        )
        db_label.pack(side=tk.RIGHT, padx=20)
        
        # --- Main Content Frame ---
        content_frame = tk.Frame(self.root, bg="#2d6093")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # --- Input Form Frame ---
        form_card = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.X, pady=(0, 10))
        
        form_title = tk.Label(
            form_card,
            text="➕ Add New Employee",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#333"
        )
        form_title.pack(pady=(10, 5))
        
        form_frame = tk.Frame(form_card, bg="white")
        form_frame.pack(pady=(0, 10), padx=20)
        
        # Input fields
        fields = [
            ("👤 Name:", 0, 0),
            ("🆔 Employee ID:", 0, 2),
            ("💰 Base Salary:", 1, 0),
            ("👔 Employee Type:", 1, 2)
        ]
        
        for label_text, row, col in fields:
            label = tk.Label(
                form_frame,
                text=label_text,
                font=("Segoe UI", 12),
                bg="white",
                fg="#555"
            )
            label.grid(row=row, column=col, padx=8, pady=6, sticky="w")
            
            if "Name" in label_text:
                self.name_entry = tk.Entry(
                    form_frame,
                    font=("Segoe UI", 10),
                    relief=tk.SOLID,
                    bd=1,
                    width=20
                )
                self.name_entry.grid(row=row, column=col+1, padx=8, pady=6)
            elif "ID" in label_text:
                self.id_entry = tk.Entry(
                    form_frame,
                    font=("Segoe UI", 10),
                    relief=tk.SOLID,
                    bd=1,
                    width=20
                )
                self.id_entry.grid(row=row, column=col+1, padx=8, pady=6)
            elif "Salary" in label_text:
                self.salary_entry = tk.Entry(
                    form_frame,
                    font=("Segoe UI", 10),
                    relief=tk.SOLID,
                    bd=1,
                    width=20
                )
                self.salary_entry.grid(row=row, column=col+1, padx=8, pady=6)
            elif "Type" in label_text:
                self.type_combobox = ttk.Combobox(
                    form_frame,
                    values=list(self.employee_classes.keys()),
                    state="readonly",
                    font=("Segoe UI", 10),
                    width=18
                )
                self.type_combobox.grid(row=row, column=col+1, padx=8, pady=6)
                self.type_combobox.set("Select Type")
        
        # Search Frame
        search_frame = tk.Frame(form_frame, bg="white")
        search_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=("Segoe UI", 12),
            bg="white",
            fg="#555"
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            relief=tk.SOLID,
            bd=1,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_employees,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # --- Button Frame ---
        button_frame = tk.Frame(form_card, bg="white")
        button_frame.pack(pady=(0, 12))
        
        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "width": 13,
            "height": 1,
            "relief": tk.FLAT,
            "cursor": "hand2"
        }
        
        buttons = [
            ("✓ Add Employee", self.add_employee, "#4CAF50"),
            ("📋 Display All", self.display_all, "#1A7AC8"),
            ("✏️ Update", self.update_employee, "#FF9800"),
            ("🗑 Clear Form", self.clear_inputs, "#9E9E9E"),
            ("❌ Delete", self.delete_employee, "#c80d00"),
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                **btn_style
            )
            btn.grid(row=0, column=i, padx=5)
        
        # --- Treeview Frame ---
        tree_card = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        tree_card.pack(fill=tk.BOTH, expand=True)
        
        tree_title = tk.Label(
            tree_card,
            text="📊 Employee Records (MySQL Database)",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333"
        )
        tree_title.pack(pady=(10, 5))
        
        tree_frame = tk.Frame(tree_card, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=28,
            fieldbackground="white",
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#2196F3",
            foreground="white"
        )
        style.map("Treeview", background=[("selected", "#1976D2")])
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "ID", "Salary", "Bonus", "Role"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)
        
        headings = [
            ("Name", 190),
            ("ID", 110),
            ("Salary", 140),
            ("Bonus", 140),
            ("Role", 170)
        ]
        
        for col, width in headings:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Total Employees: 0",
            font=("Segoe UI", 9),
            bg="#E3F2FD",
            fg="#333",
            anchor="w",
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_tree_select(self, event):
        """Populate form fields when a row is selected."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.clear_inputs()
            
            # Remove $ and commas from salary and bonus for editing
            salary_str = str(values[2]).replace('$', '').replace(',', '')
            
            self.name_entry.insert(0, values[0])
            self.id_entry.insert(0, values[1])
            self.salary_entry.insert(0, salary_str)
            
            # Handle role name mapping
            role = values[4]
            if role == "SoftwareEngineer":
                role = "Software Engineer"
            self.type_combobox.set(role)

    def add_employee(self):
        """Add employee to MySQL database."""
        if not self.db_connected:
            messagebox.showerror("Database Error", "Not connected to database!")
            return
        
        name = self.name_entry.get().strip()
        emp_id = self.id_entry.get().strip()
        salary = self.salary_entry.get().strip()
        emp_type = self.type_combobox.get().strip()

        if not name or not emp_id or not salary or emp_type == "Select Type":
            messagebox.showwarning("Input Error", "Please fill all fields correctly.")
            return

        try:
            emp_id = int(emp_id)
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Input Error", "Employee ID must be an integer and Salary must be numeric.")
            return

        # Check for duplicate ID in database
        if self.db.employee_exists(emp_id):
            messagebox.showerror("Duplicate ID", f"Employee ID {emp_id} already exists!\nPlease use a unique ID.")
            return

        if salary <= 0:
            messagebox.showerror("Input Error", "Salary must be greater than 0.")
            return

        # Calculate bonus
        bonus_rate = self.bonus_rates.get(emp_type, 0.10)
        bonus = salary * bonus_rate
        
        # Store type for database
        db_emp_type = emp_type.replace(" ", "")  # "Software Engineer" -> "SoftwareEngineer"

        # Add to database
        if self.db.add_employee(emp_id, name, salary, db_emp_type, bonus):
            messagebox.showinfo("Success", f"✓ {name} added successfully as {emp_type}!")
            self.clear_inputs()
            self.display_all()
        else:
            messagebox.showerror("Error", "Failed to add employee to database.")

    def update_employee(self):
        """Update selected employee in MySQL database."""
        if not self.db_connected:
            messagebox.showerror("Database Error", "Not connected to database!")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to update.")
            return
        
        name = self.name_entry.get().strip()
        emp_id = self.id_entry.get().strip()
        salary = self.salary_entry.get().strip()
        emp_type = self.type_combobox.get().strip()

        if not name or not emp_id or not salary or emp_type == "Select Type":
            messagebox.showwarning("Input Error", "Please fill all fields correctly.")
            return

        try:
            emp_id = int(emp_id)
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Input Error", "Employee ID must be an integer and Salary must be numeric.")
            return

        if salary <= 0:
            messagebox.showerror("Input Error", "Salary must be greater than 0.")
            return

        # Calculate bonus
        bonus_rate = self.bonus_rates.get(emp_type, 0.10)
        bonus = salary * bonus_rate
        
        db_emp_type = emp_type.replace(" ", "")

        confirm = messagebox.askyesno("Confirm Update", f"Update employee {name}?")
        if confirm:
            if self.db.update_employee(emp_id, name, salary, db_emp_type, bonus):
                messagebox.showinfo("Success", "Employee updated successfully!")
                self.clear_inputs()
                self.display_all()
            else:
                messagebox.showerror("Error", "Failed to update employee.")

    def delete_employee(self):
        """Delete selected employee from MySQL database."""
        if not self.db_connected:
            messagebox.showerror("Database Error", "Not connected to database!")
            return
        
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to delete.")
            return
        
        item = self.tree.item(selected[0])
        emp_id = int(item['values'][1])
        emp_name = item['values'][0]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {emp_name}?")
        if confirm:
            if self.db.delete_employee(emp_id):
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.clear_inputs()
                self.display_all()
            else:
                messagebox.showerror("Error", "Failed to delete employee.")

    def search_employees(self):
        """Search employees in the database."""
        if not self.db_connected:
            messagebox.showerror("Database Error", "Not connected to database!")
            return
        
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.display_all()
            return
        
        results = self.db.search_employees(search_term)
        
        # Clear treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Display search results
        for i, emp_data in enumerate(results):
            emp_id, name, salary, emp_type, bonus = emp_data
            
            display_type = emp_type
            if emp_type == "SoftwareEngineer":
                display_type = "Software Engineer"
            
            values = (
                name,
                emp_id,
                f"${salary:,.2f}",
                f"${bonus:,.2f}",
                display_type
            )
            
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='white')
        
        self.status_bar.config(text=f"Search Results: {len(results)} employee(s) found")

    def display_all(self):
        """Display all employees from MySQL database."""
        if not self.db_connected:
            return
        
        # Clear treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Fetch all employees from database
        employees = self.db.get_all_employees()
        
        for i, emp_data in enumerate(employees):
            emp_id, name, salary, emp_type, bonus = emp_data
            
            # Convert type for display
            display_type = emp_type
            if emp_type == "SoftwareEngineer":
                display_type = "Software Engineer"
            
            values = (
                name,
                emp_id,
                f"${salary:,.2f}",
                f"${bonus:,.2f}",
                display_type
            )
            
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='white')
        
        self.update_status_bar()

    def clear_inputs(self):
        """Clear all input fields."""
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        self.type_combobox.set("Select Type")
        self.search_entry.delete(0, tk.END)

    def update_status_bar(self):
        """Update status bar with current employee count from database."""
        if self.db_connected:
            total = self.db.get_employee_count()
            self.status_bar.config(text=f"Connected to MySQL | Total Employees: {total}")
        else:
            self.status_bar.config(text="Database Disconnected")

    def on_closing(self):
        """Handle window close event."""
        if self.db_connected:
            self.db.disconnect()
        self.root.destroy()


# ---------------- Main Program ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()