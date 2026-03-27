import os
import datetime
from functools import wraps

from flask import Flask, jsonify, request
import jwt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SECRET = os.getenv("FLASK_SECRET", "dev_only_secret_change_me")
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "30"))
ALGORITHM = "HS256"

# =========================
# Helper: Create JWT token
# =========================
def create_access_token(username: str, role: str):
    now = datetime.datetime.utcnow()
    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
        "iss": "itsa5504.lab6"
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

# =========================
# Decorator: Token Required
# =========================
def token_required(roles=None):
    roles = roles or []

    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401

            token = auth_header.split(" ", 1)[1].strip()

            try:
                decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            # IAM role check simulation
            user_role = decoded.get("role")
            if roles and user_role not in roles:
                return jsonify({"error": "Forbidden: insufficient role"}), 403

            request.user = decoded
            return fn(*args, **kwargs)

        return decorated

    return wrapper

# =========================
# ROUTES
# =========================

@app.get("/")
def home():
    return jsonify({"status": "ok", "service": "ITSA-5504 Lab 6 API"})

@app.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    password = body.get("password")
    role = body.get("role", "user")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    if role not in ["admin", "user"]:
        role = "user"

    token = create_access_token(username=username, role=role)
    return jsonify({"access_token": token, "token_type": "Bearer", "role": role})

@app.get("/secure")
@token_required()
def secure():
    return jsonify({"message": "You are authorized to access /secure", "claims": request.user})

@app.get("/secure-admin")
@token_required(roles=["admin"])
def secure_admin():
    return jsonify({"message": "Welcome, admin! You can access /secure-admin", "claims": request.user})

# =========================
# Run Flask (with HTTPS)
# =========================
if __name__ == "__main__":
    cert_file = "cert.pem"
    key_file = "key.pem"

    if os.path.exists(cert_file) and os.path.exists(key_file):
        app.run(host="127.0.0.1", port=5000, ssl_context=(cert_file, key_file))
    else:
        app.run(host="127.0.0.1", port=5000)