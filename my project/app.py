from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change 'your_secret_key' to a strong, random key

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER, sold INTEGER)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    item_quantity = request.form.get('item_quantity')

    if item_name and item_price and item_quantity:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO items (name, price, quantity, sold) VALUES (?, ?, ?, ?)', (item_name, item_price, item_quantity, 0))
        conn.commit()
        conn.close()
    else:
        flash('Please fill in all fields.')

    return redirect('/')

@app.route('/mark_sold/<int:item_id>', methods=['POST'])
def mark_sold(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check the current quantity of the item
    cursor.execute('SELECT quantity FROM items WHERE id = ?', (item_id,))
    item_quantity = cursor.fetchone()[0]

    if item_quantity > 0:
        # Decrement the quantity by 1 and mark as sold
        cursor.execute('UPDATE items SET sold = 1, quantity = ? WHERE id = ?', (item_quantity - 1, item_id))
        conn.commit()
    else:
        flash('Item quantity is already 0.')

    conn.close()

    return redirect('/')

if __name__ == '__main__':
    create_table()
    app.run()
