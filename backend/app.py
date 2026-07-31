"""
app.py
Flask application: API routes and business logic for the
Bank Management System backend.
"""


from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from mysql.connector import Error

from db import get_connection

app = Flask(__name__)
CORS(app)  # allows the frontend (served separately by Nginx) to call this API


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    balance = data.get("balance", 0)

    # --- Validation ---
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    try:
        balance = float(balance)
        if balance < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"message": "Balance must be a non-negative number"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"message": "Username already exists"}), 409

        cursor.execute(
            "INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)",
            (username, hashed_password.decode("utf-8"), balance),
        )
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201

    except Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            return jsonify({"message": "Invalid username or password"}), 401

        return jsonify({"message": "Login successful"}), 200

    except Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/balance/<username>", methods=["GET"])
def balance(username):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT balance FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"balance": float(user["balance"])}), 200

    except Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/health", methods=["GET"])
def health():
    """Simple endpoint to confirm the API is up (useful for manual testing)."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
