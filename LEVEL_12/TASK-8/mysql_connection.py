import pandas as pd
import time
from sqlalchemy import create_engine, text
import pyodbc
import urllib

host = "localhost"
user = "root"
password = "root"  
database = "task"


query = """
SELECT o.order_id, c.customer_name, o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_id IS NOT NULL
"""

print("\n Connecting using SQLAlchemy...")

try:
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    start = time.time()
    df_sqlalchemy = pd.read_sql(text(query), engine.connect())
    print(f" SQLAlchemy - Query Time: {round(time.time() - start, 2)}s")
    print(df_sqlalchemy.head())
    df_sqlalchemy.to_csv("high_value_orders_sqlalchemy.csv", index=False)
    print(" Data exported to high_value_orders_sqlalchemy.csv")
except Exception as e:
    print(" Error:", e)


print("\n Connecting using pyodbc (via SQLAlchemy)...")

try:
    driver = 'MySQL ODBC 9.2 Unicode Driver'
    encoded = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={host};DATABASE={database};UID={user};PWD={password}")
    engine_pyodbc = create_engine(f"mysql+pyodbc:///?odbc_connect={encoded}")

    start = time.time()
    df_pyodbc = pd.read_sql(text(query), engine_pyodbc.connect())
    print(f" pyodbc - Query Time: {round(time.time() - start, 2)}s")
    print(df_pyodbc.head())
    df_pyodbc.to_csv("high_value_orders_pyodbc.csv", index=False)
    print(" Data exported to high_value_orders_pyodbc.csv")
except Exception as e:
    print(" Error:", e)


print("\n Connecting using psycopg2 (For PostgreSQL Only)...")
print(" Skipping as MySQL is used, not PostgreSQL.")
