import os
from functools import wraps
from flask import request, jsonify, g
import jwt
from sqlalchemy.exc import NoResultFound

from db.models.user import User


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token", None)
        secret = os.environ.get("SESSION_SECRET")
        if token:
            try:
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                user_id = payload["id"]
                if user_id:
                    g.user = User.query.filter(User.id == user_id).one()
                    return func(*args, **kwargs)

            except NoResultFound:
                return jsonify({"error": "No user found with provided token"}), 403
            except Exception as e:
                return func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper
