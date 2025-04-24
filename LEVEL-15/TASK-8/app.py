from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# Update your MySQL connection details here
db_user = 'root'          # your MySQL username
db_password = 'root'  # your MySQL password
db_host = 'localhost'
db_name = 'shopping_db'

# Database connection
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# Home page route
@app.route('/')
def home():
    return '<h1>Welcome! Go to <a href="/monthly_sales">Monthly Sales Report</a></h1>'

# Monthly Sales page
@app.route('/monthly_sales')
def monthly_sales():
    query = """
        SELECT 
            DATE_FORMAT(i.invoice_date, '%%Y-%%m') AS month,
            SUM(ii.quantity * p.price) AS total_sales
        FROM invoices i
        JOIN invoice_items ii ON i.invoice_no = ii.invoice_no
        JOIN products p ON ii.product_id = p.product_id
        GROUP BY month
        ORDER BY month
    """
    df = pd.read_sql(query, engine)

    # Pass data to template
    return render_template('monthly_sales.html', data=df)

if __name__ == '__main__':
    app.run(debug=True)
