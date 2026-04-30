from abc import ABC, abstractmethod

#Salary Class (Composition)
class Salary:
    def __init__(self, base_salary):
        self.__base_salary = base_salary   # encapsulation

    def get_salary(self):
        return self.__base_salary

    def set_salary(self, new_salary):
        if new_salary > 0:
            self.__base_salary = new_salary
        else:
            print("Invalid Salary!")


#Abstract Employee Class
class Employee(ABC):
    def __init__(self, name, emp_id, salary : Salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    @abstractmethod
    def calculate_bonus(self):
        pass3

    def display_info(self):
        print(f"\nName: {self.name}")
        print(f"ID: {self.emp_id}")
        print(f"Base Salary: {self.salary.get_salary()}")
        print(f"Bonus: {self.calculate_bonus()}")


#Manager Class
class Manager(Employee):
    def __init__(self):
        name = input("Enter Manager Name: ")
        emp_id = int(input("Enter Manager ID: "))
        base_salary = float(input("Enter Manager Base Salary: "))
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.20


#Developer Class
class Developer(Employee):
    def __init__(self):
        name = input("Enter Developer Name: ")
        emp_id = int(input("Enter Developer ID: "))
        base_salary = float(input("Enter Developer Base Salary: "))
        salary_obj = Salary(base_salary)
        super().__init__(name, emp_id, salary_obj)

    def calculate_bonus(self):
        return self.salary.get_salary() * 0.10


class EmployeeManagementSystem:
    def __init__(self):
        self.employees = []

    def add_employee(self):
        emp_type = input("\nEnter Employee Type (Manager/Developer): ").strip().lower()
        
        if emp_type == "manager":
            emp = Manager()
        elif emp_type == "developer":
            emp = Developer()
        else:
            print("Invalid Employee Type!")
            return
        
        self.employees.append(emp)
        print(f"\n {emp.name} added successfully!\n")

    def display_all(self):
        if not self.employees:
            print("\nNo employees found!\n")
        else:
            print("\n----- All Employees -----")
            for emp in self.employees:
                emp.display_info()

    def run(self):
        while True:
            print("\n Employee Management System")
            print("Choose an option:")
            print("'1' For 'Add Employee'")
            print("'2' For 'Display All Employees'")
            print("'3' For 'Exit'")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.display_all()
            elif choice == "3":
                print("\nExiting Program... Goodbye!\n")
                break
            else:
                print("Invalid choice! Try again.")


# ---------------- Main Program ----------------
if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.run()

