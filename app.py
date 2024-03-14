from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
DATABASE = 'products.db'


def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            img_url TEXT NOT NULL,
            vendor TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


create_db()  # Initialize the database when the app starts


@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()

    product_list = []
    for product in products:
        product_dict = {'id': product[0], 'name': product[1], 'price': product[2], 'img_url': product[3], 'vendor': product[4]}
        product_list.append(product_dict)

    return jsonify({'products': product_list})


@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data['name']
    price = data['price']
    img_url = data['img_url']
    vendor = data['vendor']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, img_url, vendor ) VALUES (?, ?, ?, ?)', (name, price, img_url, vendor))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Product added successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
