#!/usr/bin/env python3
""" Module of session auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """route for auth session login"""
    user_email = request.form.get("email")
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    user_pwd = request.form.get("password")
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": user_email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    for detail in user:
        if detail.is_valid_password(user_pwd):
            from api.v1.app import auth
            session_id = auth.create_session(detail.id)
            user_json = jsonify(detail.to_json())
            user_json.set_cookie(getenv("SESSION_NAME"), session_id)
            return user_json
        else:
            return jsonify({"error": "wrong password"}), 401
