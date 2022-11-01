import os
import jwt


def make_token(user_id):
    return jwt.encode({"id": user_id}, os.environ.get("SESSION_SECRET"), algorithm="HS256")
