import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from PIL import Image, ImageTk
import io
import base64

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


# ---------------- Employee Management System (Enhanced GUI) ----------------
class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("900x550")
        self.root.configure(bg="#306ca7")
        self.employees = []
        self.used_ids = set()  # Track used employee IDs
        
        # Employee type to class mapping
        self.employee_classes = {
            "Manager": Manager,
            "Developer": Developer,
            "HR": HR,
            "Software Engineer": SoftwareEngineer,
            "Analyst": Analyst,
            "Designer": Designer
        }
        
        self.create_ui()

    def create_placeholder_image(self):
        """Create a simple placeholder image for the header."""
        try:
            # Create a simple gradient-like image
            width, height = 60, 60
            from PIL import Image, ImageDraw
            
            img = Image.new('RGB', (width, height), color="#3E2D9B")
            draw = ImageDraw.Draw(img)
            
            # Draw a simple user icon
            # Circle for head
            draw.ellipse([18, 12, 42, 36], fill='white', outline='white')
            # Body
            draw.ellipse([12, 33, 48, 57], fill='white', outline='white')
            
            return ImageTk.PhotoImage(img)
        except:
            return None

    def create_ui(self):
        """Create enhanced UI components."""
        
        # --- Header Frame (SMALLER) ---
        header_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_container = tk.Frame(header_frame, bg="#2196F3")
        title_container.pack(expand=True)
        
        # Try to create and display icon
        try:
            icon_image = self.create_placeholder_image()
            if icon_image:
                icon_label = tk.Label(title_container, image=icon_image, bg="#22283C")
                icon_label.image = icon_image  # Keep a reference
                icon_label.pack(side=tk.LEFT, padx=10)
        except:
            pass
        
        title = tk.Label(
            title_container, 
            text="EMPLOYEE MANAGEMENT SYSTEM", 
            font=("Segoe UI", 30, "bold"),
            bg="#2196F3",
            fg="black"
        )
        title.pack(side=tk.LEFT, padx=10)
        
        # --- Main Content Frame ---
        content_frame = tk.Frame(self.root, bg="#2d6093")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # --- Input Form Frame (COMPACT) ---
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
        
        # Styled input fields in a more compact grid
        fields = [
            ("👤 Name:", 0, 0),
            ("🆔 Employee ID:", 0, 2),
            ("💰 Base Salary:", 1, 0),
            ("👔 Employee Type:", 1, 2)
        ]
        
        self.entries = {}
        
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
        
        # --- Button Frame (COMPACT) ---
        button_frame = tk.Frame(form_card, bg="white")
        button_frame.pack(pady=(0, 12))
        
        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "width": 13,
            "height": 1,
            "relief": tk.FLAT,
            "cursor": "hand2"
        }
        
        add_btn = tk.Button(
            button_frame,
            text="✓ Add Employee",
            command=self.add_employee,
            bg="#4CAF50",
            fg="white",
            **btn_style
        )
        add_btn.grid(row=0, column=0, padx=5)
        
        display_btn = tk.Button(
            button_frame,
            text="📋 Display All",
            command=self.display_all,
            bg="#1A7AC8",
            fg="white",
            **btn_style
        )
        display_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑 Clear Form",
            command=self.clear_inputs,
            bg="#FF5B5B",
            fg="white",
            **btn_style
        )
        clear_btn.grid(row=0, column=2, padx=5)
        
        delete_btn = tk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_employee,
            bg="#c80d00",
            fg="white",
            **btn_style
        )
        delete_btn.grid(row=0, column=3, padx=5)
        
        # --- Treeview Frame (LARGER and VISIBLE) ---
        tree_card = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        tree_card.pack(fill=tk.BOTH, expand=True)
        
        tree_title = tk.Label(
            tree_card,
            text="📊 Employee Records",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333"
        )
        tree_title.pack(pady=(10, 5))
        
        # Treeview with scrollbar
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

    def add_employee(self):
        """Add employee with unique ID validation."""
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

        # Check for duplicate ID (Primary Key constraint)
        if emp_id in self.used_ids:
            messagebox.showerror("Duplicate ID", f"Employee ID {emp_id} already exists!\nPlease use a unique ID.")
            return

        if salary <= 0:
            messagebox.showerror("Input Error", "Salary must be greater than 0.")
            return

        # Create employee object
        employee_class = self.employee_classes.get(emp_type)
        if employee_class:
            emp = employee_class(name, emp_id, salary)
            self.employees.append(emp)
            self.used_ids.add(emp_id)
            
            messagebox.showinfo("Success", f"✓ {emp.name} added successfully as {emp_type}!")
            self.clear_inputs()
            self.display_all()
            self.update_status_bar()

    def delete_employee(self):
        """Delete selected employee from the system."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to delete.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
        if confirm:
            item = self.tree.item(selected[0])
            emp_id = int(item['values'][1])
            
            # Remove from employees list and used_ids set
            self.employees = [emp for emp in self.employees if emp.emp_id != emp_id]
            self.used_ids.discard(emp_id)
            
            self.display_all()
            self.update_status_bar()
            messagebox.showinfo("Success", "Employee deleted successfully!")

    def display_all(self):
        """Display all employees in the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, emp in enumerate(self.employees):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=emp.get_info(), tags=(tag,))
        
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='white')

    def clear_inputs(self):
        """Clear all input fields."""
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
        self.type_combobox.set("Select Type")

    def update_status_bar(self):
        """Update status bar with current employee count."""
        total = len(self.employees)
        self.status_bar.config(text=f"Ready | Total Employees: {total}")


# ---------------- Main Program ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()

