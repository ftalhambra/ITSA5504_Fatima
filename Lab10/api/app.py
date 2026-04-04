from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({
        "id": 101,
        "item": "Wireless Mouse",
        "price": 29.99
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)