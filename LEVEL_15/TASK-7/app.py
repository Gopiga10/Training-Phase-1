from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# Step 1: Database connection - Replace with your actual details
username = 'root'        # your MySQL username
password = 'root'    # your MySQL password
host = 'localhost'       # or '127.0.0.1'
database = 'shopping_db'  # your database name

# Create engine
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

@app.route('/')
def home():
    return '<h2>Welcome! Go to <a href="/report">Report Page</a></h2>'

@app.route('/report')
def report():
    try:
        # Step 2: Query your table (replace with your actual table name)
        query = "SELECT * FROM customer_shopping LIMIT 25"

        df = pd.read_sql(query, engine)

        # Step 3: Convert DataFrame to HTML table
        table_html = df.to_html(classes='table table-bordered table-striped', index=False)

        return render_template('report.html', table=table_html)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
