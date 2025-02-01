import streamlit as st
import os
import sqlite3
import google.generativeai as gen
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable")
    st.stop()

gen.configure(api_key=GOOGLE_API_KEY)

# Function to create tables if they don't exist
def create_tables(db_path="company.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Department TEXT NOT NULL,
            Salary REAL NOT NULL,
            Hire_Date TEXT NOT NULL
        )
    """)

    # Create departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE,
            Manager TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Ensure tables exist at app startup
create_tables()

# Function to get Gemini response
def get_gemini_response(question, prompt):
    model = gen.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query and return results
def read_sql_query(sql, db_path="company.db"):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

# SQL prompt for Gemini AI
prompt = [
    """
    You are an expert in converting English Questions to SQL query!
    The SQL database has 2 tables - employees and departments.
    
    Table employees columns:
    - ID
    - Name
    - Department
    - Salary
    - Hire_Date
    
    Table departments columns:
    - ID
    - Name
    - Manager
    
    The Department in employees table corresponds to the Name in departments table.
    
    Example queries:
    1. Show me all employees in the marketing department
    SELECT e.* FROM employees e WHERE e.Department = "Marketing";
    
    2. Who is the manager of the marketing department?
    SELECT d.Manager FROM departments d WHERE d.Name = "Marketing";
    
    3. Show me all employees and their department managers
    SELECT e.Name as Employee, e.Department, d.Manager 
    FROM employees e 
    JOIN departments d ON e.Department = d.Name;
    
    4. Show me the total salary by department with department manager
    SELECT e.Department, d.Manager, SUM(e.Salary) as Total_Salary 
    FROM employees e 
    JOIN departments d ON e.Department = d.Name 
    GROUP BY e.Department;
    
    The SQL code should not have ''' in beginning or end and sql word in the output
    """
]

# Streamlit UI
st.set_page_config(page_title="SQL Query Assistant")
st.header("Gemini AI - SQL Query Assistant")

# Sidebar with example queries
st.sidebar.header("Example Questions")
st.sidebar.write("""
- Show all employees in Marketing
- Who manages the IT department?
- Show all employees with their managers
- What is the total salary by department?
- Show employees hired after 2020
""")

# Display existing tables in the database
st.subheader("📋 Employees Table")
employees_df = read_sql_query("SELECT * FROM employees", "company.db")
if isinstance(employees_df, str):
    st.error(employees_df)
else:
    st.dataframe(employees_df, use_container_width=True)

st.subheader("📋 Departments Table")
departments_df = read_sql_query("SELECT * FROM departments", "company.db")
if isinstance(departments_df, str):
    st.error(departments_df)
else:
    st.dataframe(departments_df, use_container_width=True)

# User input for question
st.subheader("🔍 Ask a Question to Generate SQL Query")
question = st.text_input("Enter your question:", key="input")
submit = st.button("Generate SQL Query")

# Process the user's question
if submit:
    if question:
        response = get_gemini_response(question, prompt)
        st.subheader("🔹 Generated SQL Query:")
        st.code(response, language="sql")
        
        st.subheader("🔹 Query Results:")
        results = read_sql_query(response, "company.db")
        
        if isinstance(results, str):  # If there's an error
            st.error(results)
        else:
            st.dataframe(results, use_container_width=True)
            st.write(f"Total results: {len(results)} rows")
    else:
        st.warning("Please enter a question.")