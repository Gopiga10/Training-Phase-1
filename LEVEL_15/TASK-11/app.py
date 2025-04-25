from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from collections import defaultdict

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="shopping_db"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        email = request.form['email']
        phone = request.form['phone']
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        price = request.form['price']
        order_date = request.form['order_date']

        # Insert customer
        cursor.execute("INSERT INTO customers (customer_name, email, phone) VALUES (%s, %s, %s)",
                       (customer_name, email, phone))
        customer_id = cursor.lastrowid

        # Insert order
        cursor.execute("INSERT INTO orders (customer_id, product_name, quantity, price, order_date) VALUES (%s, %s, %s, %s, %s)",
                       (customer_id, product_name, quantity, price, order_date))

        db.commit()
        return redirect(url_for('report'))

    return render_template('input.html')

@app.route('/report')
def report():
    cursor.execute("""
        SELECT customers.customer_name, customers.email, customers.phone,
               orders.product_name, orders.quantity, orders.price, orders.order_date
        FROM customers
        JOIN orders ON customers.customer_id = orders.customer_id
    """)
    data = cursor.fetchall()
    return render_template('report.html', data=data)

@app.route('/dashboard')
def dashboard():
    # Aggregate customers by month
    cursor.execute("""
        SELECT MONTH(order_date) AS month, COUNT(DISTINCT customers.customer_id) AS customer_count
        FROM orders
        JOIN customers ON customers.customer_id = orders.customer_id
        GROUP BY MONTH(order_date)
        ORDER BY MONTH(order_date)
    """)
    data = cursor.fetchall()

    # Prepare data for the chart
    months = [row[0] for row in data]
    customer_counts = [row[1] for row in data]

    return render_template('dashboard.html', months=months, customer_counts=customer_counts)

if __name__ == '__main__':
    app.run(debug=True)
