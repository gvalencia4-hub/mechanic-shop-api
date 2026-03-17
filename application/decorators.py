from functools import wraps
from flask import request, jsonify
from application.utils import decode_token


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing token"}), 401

        try:
            token = auth_header.split(" ")[1]
            data = decode_token(token)
            customer_id = int(data["sub"])
        except Exception:
            return jsonify({"error": "Invalid token"}), 401

        return f(customer_id, *args, **kwargs)

    return wrapper