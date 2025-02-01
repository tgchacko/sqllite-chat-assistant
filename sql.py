import sqlite3

def create_and_insert_data(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS Employees')
        cursor.execute('DROP TABLE IF EXISTS Departments')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                Department_ID INTEGER PRIMARY KEY,
                Name TEXT UNIQUE,
                Manager TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                Employee_ID INTEGER PRIMARY KEY,
                Name TEXT,
                Department TEXT,
                Salary INTEGER,
                Hire_Date TEXT,
                FOREIGN KEY (Department) REFERENCES Departments(Name)
            )
        ''')
        
        departments_data = [
            (1, 'Sales', 'John Smith'),
            (2, 'Engineering', 'Jane Doe'),
            (3, 'Marketing', 'Mike Johnson'),
            (4, 'IT', 'Sarah Wilson'),
            (5, 'HR', 'Tom Brown')
        ]
        cursor.executemany("INSERT INTO Departments VALUES (?, ?, ?)", departments_data)
        
        employees_data = [
            (1, 'John Smith', 'Sales', 60000, '2020-01-01'),
            (2, 'Alice Johnson', 'Sales', 50000, '2021-01-15'),
            (3, 'Bob Wilson', 'Sales', 52000, '2021-02-20'),
            (4, 'Jane Doe', 'Engineering', 80000, '2019-01-01'),
            (5, 'Edward Clark', 'Engineering', 70000, '2020-03-15'),
            (6, 'Fiona Gray', 'Engineering', 72000, '2020-04-10'),
            (7, 'Mike Johnson', 'Marketing', 65000, '2018-01-01'),
            (8, 'Helen Brown', 'Marketing', 60000, '2022-01-05'),
            (9, 'Ivy Green', 'Marketing', 62000, '2022-02-15'),
            (10, 'Sarah Wilson', 'IT', 70000, '2017-01-01'),
            (11, 'Liam Brown', 'IT', 65000, '2021-11-20'),
            (12, 'Tom Brown', 'HR', 55000, '2016-01-01')
        ]
        cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?)", employees_data)
        
        conn.commit()
        print(f"Database '{database_name}' created successfully with tables and sample data")
        
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

create_and_insert_data("company.db")