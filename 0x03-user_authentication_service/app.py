#!/usr/bin/env python3
"""
a basic flask app
Start the home session
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """home route of the application"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """register a user/users"""
    email = request.form.get("email")
    passwd = request.form.get("password")

    try:
        AUTH.register_user(email, passwd)
        return jsonify({"email": email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """logout function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """profile function"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user or session_id is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """get the reset token to reset password"""
    try:
        email = request.form.get("email")
        r_token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": r_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """update_password function to respond to reset_password
    route"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, password)
    except Exception:
        abort(403)
    return jsonify({"email": email,
                    "message": "Password updated"
                    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
