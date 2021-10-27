from functools import wraps

import jwt
from flask import request, current_app


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not (token := request.headers.get("x-access-tokens")):
            return "Token is missing.", 403

        db = current_app.config["USER_DATABASE_SERVICE"]
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], verify=False)
        except jwt.DecodeError:
            return "Token is invalid.", 403
        if current_user := db.get_user_by_id(data.get("public_id")):
            return f(current_user, *args, **kwargs)
        return "Token is invalid.", 403
    return decorator
