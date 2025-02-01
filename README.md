# Chat Assistant for SQLite Database with Gemini AI

A Streamlit-based web application that converts natural language questions into SQL queries and executes them using Google's Gemini AI. The application helps users interact with a SQLite database using plain English instead of writing SQL queries directly.

## Demo
Access the live application here: [Chat Assistant for SQLite Database with Gemini AI](https://sqllite-chat-assistant.streamlit.app)

## Features
- Natural language to SQL query conversion
- Interactive web interface built with Streamlit
- Support for complex queries across multiple tables
- Real-time query execution and result display
- Sample database with employees and departments data
- Secure API key handling

## Project Structure
```
sql-query-assistant/
├── app.py                 # Main Streamlit application
├── database_setup.py      # Database creation and sample data
├── requirements.txt       # Project dependencies
├── .env.example          # Example environment variables file
├── .gitignore            # Git ignore rules
├── Procfile              # Streamlit deployment configuration
├── runtime.txt           # Python runtime specification
├── setup.sh              # Streamlit configuration
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tgchacko/sqllite-chat-assistant.git
cd sql-query-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your Google API key to the `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Create the database:
```bash
python database_setup.py
```

6. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Start the application and navigate to the provided URL (typically http://localhost:8501)
2. Enter your question in natural language, for example:
   - "Show all employees in Marketing"
   - "Who manages the IT department?"
   - "What is the total salary by department?"
3. Click "Ask the question" to see the:
   - Generated SQL query
   - Query results in a formatted table

## Database Schema

### Employees Table
- ID (INTEGER PRIMARY KEY)
- Name (TEXT)
- Department (TEXT)
- Salary (INTEGER)
- Hire_Date (TEXT)

### Departments Table
- ID (INTEGER PRIMARY KEY)
- Name (TEXT UNIQUE)
- Manager (TEXT)

## Known Limitations

1. Query Complexity
   - The AI may struggle with very complex queries
   - Some advanced SQL features might not be properly interpreted

2. Database Constraints
   - Currently uses SQLite, which may not be suitable for production workloads
   - Database is recreated on each deployment to Streamlit

3. Performance
   - Response time depends on Gemini AI API latency
   - Limited by Streamlit free tier constraints

## Suggestions for Improvement

1. Database Enhancements
   - Migrate to a production-grade database like PostgreSQL
   - Add more tables and relationships

2. Features
   - Add query history
   - Implement user authentication
   - Add query validation before execution
   - Include data visualization options

3. Security
   - Implement rate limiting
   - Add input validation
   - Set up proper logging
   - Add API key rotation

4. UI/UX
   - Add more example queries
   - Implement query templates
   - Add export functionality for results
   - Improve error messages and feedback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for natural language processing
- Streamlit for the web interface and hosting

## Contact

Your Name - tharakhgeorge@yahoo.co.in
<<<<<<< HEAD
Project Link: https://github.com/tgchacko/sqllite-chat-assistant
=======
Project Link: [https://github.com/tgchacko/chat-assistant-sqlite](https://github.com/tgchacko/sqllite-chat-assistant)
>>>>>>> 4803a8c88fc68191f56c735b66e70635027db2f9
