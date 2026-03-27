from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_root():
    return "Hello Cloud from Flask (root)!"

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/hello")
def hello():
    return jsonify(message="Hello from the containerized Flask app")

# This is what the gateway will front as /api
@app.route("/api")
def api():
    return jsonify(service="flask", message="Hello from /api inside Flask")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)