#!/usr/bin/env python3
""" Module of sesion auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST /auth_session/login
    handles all routes for the Session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({'error': "email missing"}), 400
    elif password is None:
        return jsonify({'error': "password missing"}), 400
    user = User.search({"email": email})
    if not user or user == []:
        return jsonify({'error': "no user found for this email"}), 404
    for use in user:
        if use.is_valid_password(password):
            return jsonify({'error': "wrong password"}), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(use.id)
            response = jsonify(use.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_auth_session() -> str:
    """ POST /auth_session/login
    handles all routes for the Session authentication
    """
    from api.v1.app import auth
    session_id = auth.destroy_session(request)
    if session_id is False:
        abort(404)
    return jsonify({}), 200
