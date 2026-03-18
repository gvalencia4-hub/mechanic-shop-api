from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from . import customers_bp
from .schemas import customer_schema, customers_schema
from ...extensions import db
from ...models import Customer


@customers_bp.route("/", methods=["POST"])
def create_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers
    summary: Create customer
    description: Creates a new customer in the system.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            name:
              type: string
              example: Jane Doe
            email:
              type: string
              example: jane@email.com
            phone:
              type: string
              example: 555-123-4567
    responses:
      201:
        description: Customer created successfully
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: Jane Doe
            email:
              type: string
              example: jane@email.com
            phone:
              type: string
              example: 555-123-4567
      400:
        description: Validation error
      500:
        description: Server error
    """
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


@customers_bp.route("/", methods=["GET"])
def get_customers():
    """
    Get all customers
    ---
    tags:
      - Customers
    summary: Get customers
    description: Returns all customers.
    responses:
      200:
        description: List of customers
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: Jane Doe
              email:
                type: string
                example: jane@email.com
              phone:
                type: string
                example: 555-123-4567
    """
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200