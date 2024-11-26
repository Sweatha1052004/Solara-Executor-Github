import sqlite3
import pandas as pd

# Connect to (or create) the SQLite database
connection = sqlite3.connect("students.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Define the SQL query to create the STUDENTS table (excluding Register_Number)
table_info = """
CREATE TABLE IF NOT EXISTS STUDENTS (
    S_No INT,
    Portal_ID VARCHAR(50),
    Name VARCHAR(255),
    Department VARCHAR(100),
    C_Course VARCHAR(100),
    L1_Score INT,
    L2_Score INT,
    L3_Score INT,
    L4_Score INT,
    L5_Score INT,
    L6_Score INT,
    L7_Score INT,
    L8_Score INT,
    DS INT,
    PDS INT,
    DBMS INT,
    Java_Collections INT,
    Weekly_Test_Total_Score INT,
    Total_Score INT,
    Total_Diff INT,
    RANK INT
);
"""

# Execute the SQL query to create the table
cursor.execute(table_info)

# Path to the CSV file (replace with your actual file path)
csv_file = r"C:\Users\Admin\Desktop\Txt_to_sql\Students Performance csv.csv"

# Read the CSV file into a DataFrame
data = pd.read_csv(csv_file)

# Drop the 'Register_Number' column from the DataFrame
data = data.drop(columns=["Register_Number"])

# Ensure DataFrame column names match the table schema
data.columns = [
    "S_No", "Portal_ID", "Name", "Department", "C_Course",
    "L1_Score", "L2_Score", "L3_Score", "L4_Score", "L5_Score",
    "L6_Score", "L7_Score", "L8_Score", "DS", "PDS",
    "DBMS", "Java_Collections", "Weekly_Test_Total_Score",
    "Total_Score", "Total_Diff", "RANK"
]

# Insert the data into the STUDENTS table
data.to_sql("STUDENTS", connection, if_exists="append", index=False)

# Commit the transaction and close the connection
connection.commit()
connection.close()

print("Database 'students.db' created successfully, and data has been inserted.")
