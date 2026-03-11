from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from . import customers_bp
from .schemas import customer_schema, customers_schema
from ...extensions import db
from ...models import Customer


@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200


@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return customer_schema.jsonify(customer), 200


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


@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        customer_data = customer_schema.load(request.json)

        customer.name = customer_data["name"]
        customer.email = customer_data["email"]
        customer.phone = customer_data["phone"]

        db.session.commit()

        return customer_schema.jsonify(customer), 200

    except ValidationError as err:
        return jsonify(err.messages), 400


@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": f"Customer {id} deleted successfully"}), 200