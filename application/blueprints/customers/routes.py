from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from . import customers_bp
from .schemas import customer_schema, customers_schema
from ...extensions import db, limiter, cache
from ...models import Customer
from ...utils import encode_token


@customers_bp.route("/", methods=["GET"])
@cache.memoize(timeout=60)
def get_customers():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=5, type=int)

    query = select(Customer)
    customers = db.paginate(query, page=page, per_page=per_page, error_out=False)

    return jsonify({
        "items": customers_schema.dump(customers.items),
        "page": customers.page,
        "per_page": customers.per_page,
        "total": customers.total,
        "pages": customers.pages
    }), 200


@customers_bp.route("/", methods=["POST"])
def create_customer():
    try:
        new_customer = customer_schema.load(request.json)

        db.session.add(new_customer)
        db.session.commit()

        return customer_schema.jsonify(new_customer), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        customer_data = request.json

        customer.name = customer_data["name"]
        customer.email = customer_data["email"]
        customer.phone = customer_data["phone"]

        if "password" in customer_data:
            customer.password = customer_data["password"]

        db.session.commit()

        return customer_schema.jsonify(customer), 200

    except ValidationError as err:
        return jsonify(err.messages), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": f"Customer {id} deleted successfully"}), 200


@customers_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter_by(email=email).first()

    if not customer or customer.password != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(customer.id)

    return jsonify({"token": token}), 200