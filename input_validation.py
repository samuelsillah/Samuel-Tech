#This program is how you can you can connect your SQL Server in python, you can write and read data in SQL as well in python

import pyodbc

# Connection Details
server = 'your-servername'
database = 'DatabaseName'
driver = '{Drivername}'  # Adjust based on your installed driver

# Connect to SQL Server (Windows Authentication)
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
print("Connection successful!")

cursor = conn.cursor()

# 1. CREATE TABLE (if not exists)
create_table_query = '''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Employee' AND xtype='U')
CREATE TABLE Employee (
    ID INT PRIMARY KEY,
    Name NVARCHAR(50),
    Age INT,
    Department NVARCHAR(50)
)
'''
cursor.execute(create_table_query)
conn.commit()
print("Table ready!")


# Check if Employee Exists by ID
def employee_exists(emp_id):
    cursor.execute('SELECT COUNT(*) FROM Employee WHERE ID = ?', (emp_id,))
    return cursor.fetchone()[0] > 0


# INSERT EMPLOYEE
def insert_employee():
    emp_id = int(input("Enter Employee ID: "))

    # Check if Employee Exists
    if employee_exists(emp_id):
        print(f"Employee with ID {emp_id} already exists!")
        return

    name = input("Enter Employee Name: ")
    age = int(input("Enter Employee Age: "))
    department = input("Enter Department: ")

    insert_query = '''
    INSERT INTO Employee (ID, Name, Age, Department) VALUES (?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (emp_id, name, age, department))
    conn.commit()
    print(f"Employee {name} inserted successfully!")


# READ EMPLOYEES
def read_employees():
    cursor.execute('SELECT * FROM Employees')
    print("\n--- Employees ---")
    rows = cursor.fetchall()
    if not rows:
        print("No employee found.")
        return
    
    for row in rows:
        print(f"ID: {row.ID}, Name: {row.Name}, Age: {row.Age}, Department: {row.Department}")


# UPDATE EMPLOYEE
def update_employee():
    emp_id = int(input("Enter Employee ID to update: "))

    if not employee_exists(emp_id):
        print(f"Employee with ID {emp_id} does not exist!")
        return

    new_name = input("Enter new name (leave blank to skip): ")
    new_age = input("Enter new age (leave blank to skip): ")
    new_department = input("Enter new department (leave blank to skip): ")

    update_query = 'UPDATE Employees SET '
    updates = []

    if new_name:
        updates.append(f"Name = '{new_name}'")
    if new_age:
        updates.append(f"Age = {int(new_age)}")
    if new_department:
        updates.append(f"Department = '{new_department}'")

    if not updates:
        print("No changes made.")
        return

    update_query += ", ".join(updates)
    update_query += f' WHERE ID = {emp_id}'

    cursor.execute(update_query)
    conn.commit()
    print(f"Employee with ID {emp_id} updated!")


# DELETE EMPLOYEE
def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))

    if not employee_exists(emp_id):
        print(f"Employee with ID {emp_id} does not exist!")
        return

    delete_query = 'DELETE FROM Employees WHERE ID = ?'
    cursor.execute(delete_query, (emp_id,))
    conn.commit()
    print(f"Employee with ID {emp_id} deleted!")


# MENU
def menu():
    while True:
        print("\n--- EMPLOYEE MANAGEMENT SYSTEM ---")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            insert_employee()
        elif choice == '2':
            read_employees()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again!")


menu()

cursor.close()
conn.close()
print("Connection closed.")
