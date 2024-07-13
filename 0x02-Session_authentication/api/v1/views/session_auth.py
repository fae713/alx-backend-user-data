#!/usr/bin/env python3
"""
A Flask view that handles all routes
for the Session authentication.
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handles the login via session authentication.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search(email)
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(
        key=os.getenv('SESSION_NAME', '_my_session_id'), value=session_id)

    return response
