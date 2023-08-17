#!/usr/bin/env python3
"""a basic flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """home route of the application"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """register a user/users"""
    email = request.form.get("email")
    passwd = request.form.get("password")

    try:
        AUTH.register_user(email, passwd)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login function on the app"""
    email = request.form.get("email")
    passwd = request.form.get("password")

    if AUTH.valid_login(email=email, password=passwd) is False:
        abort(401)
    session_id = AUTH.create_session(email=email)
    response = jsonify({
        "email": email,
        "message": "logged in"
    })
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")