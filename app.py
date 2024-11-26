import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt to instruct the Gemini model (ensure prompt is defined before being used)
prompt = [
    """
    You are an expert at converting English questions into SQL queries. You are working with a database named `STUDENTS`, which has the following structure:

    - `S_No` (integer): Serial number of the student.
    - `Portal_ID` (string): Unique portal ID for each student.
    - `Register_Number` (numeric): The register number of the student.
    - `Name` (string): The name of the student.
    - `Department` (string): The department the student belongs to.
    - `C_Course` (string): The course the student is enrolled in.
    - `L1_Score` to `L8_Score` (float): Scores for levels 1 to 8.
    - `DS` (float): Data Structures score.
    - `PDS` (float): Programming Data Structures score.
    - `DBMS` (float): Database Management Systems score.
    - `Java_Collections` (float): Java Collections score.
    - `Weekly_Test_Total_Score` (float): Total score for weekly tests.
    - `Total_score` (float): Overall total score.
    - `Total_Diff` (float): Difference in total scores.
    - `RANK` (integer): Rank of the student.

    Your task is to:
    1. Convert the user's natural language query into an optimized SQL command.
    2. Ensure the query matches the database schema and structure exactly.
    3. Execute the query on the database (if needed) and return the data in JSON format.
    4. Provide the SQL query as well as the query result.

    Examples:
    1. User Query: "Show me the names and ranks of the top 10 students."
       SQL Query: `SELECT Name, RANK FROM STUDENTS ORDER BY RANK ASC LIMIT 10;`
    """
]

# Function to load the Google Gemini model and get SQL query as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    generated_query = response.text.strip()
    print(f"Generated SQL Query: {generated_query}")  # Debugging
    return generated_query

# Streamlit app setup
st.set_page_config(page_title="Gemini SQL Assistant", page_icon="🔎")
st.header("Gemini SQL Assistant: Convert Questions to SQL Queries")

# Apply custom styling
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            border: 2px solid #4CAF50;
            font-size: 18px;
            padding: 12px;
            border-radius: 8px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stCode {
            background-color: #f4f4f4;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 16px;
        }
        .stText {
            font-size: 18px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# User input for the natural language query
question = st.text_input("Ask your question about the database:", key="input", placeholder="e.g., 'Show me the top 10 students'")

# Button to trigger the query
submit = st.button("Generate SQL Query")

# If the button is clicked
if submit:
    # Get SQL query from Gemini
    response = get_gemini_response(question, prompt)
    
    # Validate the generated query
    if response and response.strip():
        st.subheader("Generated SQL Query")
        st.code(response, language="sql")
    else:
        st.error("The model did not generate a valid SQL query. Please try again.")

# Explanation section
st.markdown("""
    <div class="stText">
        The Gemini SQL Assistant helps you convert your natural language questions into SQL queries. 
        Simply enter your question, and the tool will generate the SQL query that can be used to retrieve data from the database.
    </div>
""", unsafe_allow_html=True)
