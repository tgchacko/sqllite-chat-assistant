import sqlite3

def create_and_insert_data(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        # Drop existing tables if they exist to avoid duplicate data
        cursor.execute('DROP TABLE IF EXISTS Employees')
        cursor.execute('DROP TABLE IF EXISTS Departments')
        
        # Create Departments table first since Employees will reference it
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                ID INTEGER PRIMARY KEY,
                Name TEXT UNIQUE,  -- Adding UNIQUE constraint
                Manager TEXT
            )
        ''')
        
        # Create Employees table with foreign key constraint
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                Department TEXT,
                Salary INTEGER,
                Hire_Date TEXT,
                FOREIGN KEY (Department) REFERENCES Departments(Name)
            )
        ''')
        
        # Insert departments first
        departments_data = [
            (1, 'Sales', 'John Smith'),
            (2, 'Engineering', 'Jane Doe'),
            (3, 'Marketing', 'Mike Johnson'),
            (4, 'IT', 'Sarah Wilson'),
            (5, 'HR', 'Tom Brown')
        ]
        cursor.executemany("INSERT INTO Departments VALUES (?, ?, ?)", departments_data)
        
        # Insert employees with corresponding departments
        employees_data = [
            (1, 'Alice Johnson', 'Sales', 50000, '2021-01-15'),
            (2, 'Bob Wilson', 'Engineering', 70000, '2020-06-10'),
            (3, 'Charlie Davis', 'Marketing', 60000, '2022-03-20'),
            (4, 'Diana Miller', 'Sales', 55000, '2021-08-01'),
            (5, 'Edward Clark', 'Engineering', 75000, '2020-03-15'),
            (6, 'Fiona Gray', 'Marketing', 62000, '2022-05-10'),
            (7, 'George White', 'IT', 65000, '2021-11-20'),
            (8, 'Helen Brown', 'HR', 52000, '2022-01-05')
        ]
        cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?)", employees_data)
        
        conn.commit()
        print(f"Database '{database_name}' created successfully with tables and sample data")
        
        # Verify the data
        print("\nDepartments:")
        cursor.execute("SELECT * FROM Departments")
        print(cursor.fetchall())
        
        print("\nEmployees:")
        cursor.execute("SELECT * FROM Employees")
        print(cursor.fetchall())
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Create the database
create_and_insert_data("company.db")