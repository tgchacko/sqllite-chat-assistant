import streamlit as st
import os
import sqlite3
import google.generativeai as gen
import pandas as pd
from dotenv import load_dotenv
from sql import create_and_insert_data
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable")
    st.stop()

gen.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(question, prompt):
    model = gen.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db_path="company.db"):
    try:
        # Create database if it doesn't exist
        if not os.path.exists(db_path):
            create_and_insert_data(db_path)
            
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

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

# Streamlit App
st.set_page_config(page_title="SQL Query Assistant")
st.header("Gemini App To Retrieve SQL Data")

# Add example questions to help users
st.sidebar.header("Example Questions")
st.sidebar.write("""
- Show all employees in Marketing
- Who manages the IT department?
- Show all employees with their managers
- What is the total salary by department?
- Show employees hired after 2020
""")

question = st.text_input("Input your question:", key="input")
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    if question:
        response = get_gemini_response(question, prompt)
        st.subheader("Generated SQL Query:")
        st.code(response, language="sql")
        
        st.subheader("Query Results:")
        results = read_sql_query(response, "company.db")
        
        if isinstance(results, str):  # Error occurred
            st.error(results)
        else:
            # Display the DataFrame
            st.dataframe(
                results,
                use_container_width=True,
                hide_index=True
            )
            
            # Also show total number of results
            st.write(f"Total results: {len(results)} rows")
    else:
        st.warning("Please enter a question.")
