import os
from datetime import datetime, timedelta
from flask import jsonify, request
from sqlalchemy.exc import NoResultFound, IntegrityError
import jwt

from api import api
from db.models.user import User
from db.shared import db


@api.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    json body is expected to contain {username: required(string), password: required(string)}
    """
    data = request.get_json(force=True)
    username = data.get("username", None)
    password = data.get("password", None)

    if None in [username, password]:
        return jsonify({"error": "username and password required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "User with provided username already exists"}), 401
    except ValueError:
        return jsonify({"error": "Validation error"}), 401

    token = jwt.encode(
        {"id": user.id, "exp": datetime.now() + timedelta(days=1)},
        os.environ.get("SESSION_SECRET"),
        algorithm="HS256",
    )

    return jsonify({"username": username, "token": token})


@api.route("/login", methods=["POST"])
def login():
    """
    Authenticate an existing user
    json body is expected to contain {username: required(string), password: required(string)}
    """
    data = request.get_json(force=True)
    username = data.get("username", None)
    password = data.get("password", None)

    if None in [username, password]:
        return jsonify({"error": "username and password required"}), 400

    user = None
    try:
        user = User.query.filter(User.username == username).one()
    except NoResultFound:
        return jsonify({"error": "Wrong username and/or password"}), 401

    if not user.correct_password(password):
        return jsonify({"error": "Wrong username and/or password"}), 401

    token = jwt.encode(
        {"id": user.id, "exp": datetime.now() + timedelta(days=1)},
        os.environ.get("SESSION_SECRET"),
        algorithm="HS256",
    )

    return jsonify({"username": username, "token": token, "id": user.id})
