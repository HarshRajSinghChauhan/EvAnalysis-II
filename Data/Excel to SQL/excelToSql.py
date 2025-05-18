import pandas as pd
import pyodbc

# Load Excel file
excel_path = r"C:\Harsh R.S. Chauhan\Projects\EV Analysis\datasets\electric_vehicle_sales_by_makers.xlsx"
df = pd.read_excel(excel_path, sheet_name='electric_vehicle_sales_by_maker')

# Clean column names
df.columns = [col.strip().replace(' ', '_') for col in df.columns]

# Optional: convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# SQL Server connection string
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=HARSH\MSSQLSERVER01;"
    r"DATABASE=EvProject;"
    r"Trusted_Connection=yes;"
)

# Connect to SQL Server
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Table name
table_name = 'EV_Sales'

# Drop table if it exists
cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")

# Create new table
cursor.execute(f"""
CREATE TABLE {table_name} (
    [date] DATE,
    [vehicle_category] NVARCHAR(255),
    [maker] NVARCHAR(255),
    [electric_vehicles_sold] INT
)
""")

# Insert data
for _, row in df.iterrows():
    cursor.execute(
        f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)",
        row['date'],
        row['vehicle_category'],
        row['maker'],
        int(row['electric_vehicles_sold']) if pd.notnull(row['electric_vehicles_sold']) else None
    )

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Excel data imported into SQL Server table 'EV_Sales'.")
