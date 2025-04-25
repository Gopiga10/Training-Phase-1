from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# Replace with your actual DB credentials
db_connection = 'mysql+pymysql://root:root@localhost/shopping_db'
engine = create_engine(db_connection)

@app.route('/')
def monthly_sales():
    query = """
        SELECT 
            DATE_FORMAT(i.invoice_date, '%%Y-%%m') AS month,
            SUM(ii.quantity * p.price) AS cumulative_sales
        FROM invoices i
        JOIN invoice_items ii ON i.invoice_no = ii.invoice_no
        JOIN products p ON ii.product_id = p.product_id
        GROUP BY month
        ORDER BY month
    """
    df = pd.read_sql(query, engine)

    return render_template('monthly_sales.html', data=df)

@app.route('/top_customers')
def top_customers():
    query = """
        SELECT 
            p.category,
            c.customer_id,
            c.customer_name,
            SUM(ii.quantity * p.price) AS total_spent
        FROM invoice_items ii
        JOIN invoices i ON ii.invoice_no = i.invoice_no
        JOIN products p ON ii.product_id = p.product_id
        JOIN customers c ON i.customer_id = c.customer_id
        GROUP BY p.category, c.customer_id
        ORDER BY p.category, total_spent DESC
    """
    df = pd.read_sql(query, engine)

    # Get top 5 customers for each category
    top_customers = df.groupby('category').head(5)

    return render_template('top_customers.html', data=top_customers)

if __name__ == '__main__':
    app.run(debug=True)
