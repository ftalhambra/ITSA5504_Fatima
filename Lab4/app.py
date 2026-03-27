from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = [
        {"order_id": 1, "item": "Laptop", "price_usd": 1200},
        {"order_id": 2, "item": "Phone", "price_usd": 800},
        {"order_id": 3, "item": "Headphones", "price_usd": 150}
    ]
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)