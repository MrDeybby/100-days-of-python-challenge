import os

class Employee:
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def info(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")
    
class Manager(Employee):
    
    def __init__(self, name, salary, department):
        super().__init__(name, salary)
        self.department = department
    
    def info(self):
        super().info()
        print(f"Department: {self.department}")


class Developer(Employee):
    
    def __init__(self, name, salary, programming_language):
        super().__init__(name, salary)
        self.programming_language = programming_language
        
    def info(self):
        super().info()
        print(f"Language: {self.programming_language}")

def menu():
    print("=== Employee Manager ===")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Exit")


def create_employee():
    print("=== Add Employee ==")
    print("1. Add General Employee")
    print("2. Add Manager")
    print("3. Add Developer")
    
    choice = input("Enter your choice (1-5): ").strip()
    name = input("What is employee's name: ")
    try:
        salary = float(input("What is employee's salary: "))
    except ValueError:
        print("Salary must be in numbers")
        return
    
    if choice == "1":
        employee = Employee(name=name, salary=salary)
    elif choice == "2":
        department = input("Department: ")
        employee = Manager(name=name, salary=salary, department=department)
    elif choice == "3":
        programming_language = input("Programming Language: ")
        employee = Developer(name=name, salary=salary, programming_language=programming_language)
    else:
        return
    
    print("Employee Created")
    return employee

def main():
    employees = []
    
    while True:
        os.system("cls")
        menu()
        choice = input("Enter your choice (1-3): ").strip()
        os.system("cls")

        if choice == "1":
            employee = create_employee()
            if employee:
                employees.append(employee)
            input("Press Enter to continue...")

        elif choice == "2":
            if not employees:
                print("There are no employees on the list.")
                input("Press Enter to continue...")
                continue
            
            for employee in employees:
                employee.info()
                print("")
            input("Press Enter to continue...")
        
        elif choice == "3":
            print("Exiting the program.")
            break
            
if __name__ == "__main__":
    main()