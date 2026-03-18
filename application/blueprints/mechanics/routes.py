from flask import request, jsonify
from sqlalchemy import select, func
from marshmallow import ValidationError

from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from ...extensions import db
from ...models import Mechanic, service_mechanics


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    """
    Create a new mechanic
    ---
    tags:
      - Mechanics
    summary: Create mechanic
    description: Creates a new mechanic in the system.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@email.com
            salary:
              type: number
              example: 60000
    responses:
      201:
        description: Mechanic created successfully
        schema:
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john@email.com
            salary:
              type: number
              example: 60000
      400:
        description: Validation error
      500:
        description: Server error
    """
    try:
        new_mechanic = mechanic_schema.load(request.json)

        db.session.add(new_mechanic)
        db.session.commit()

        return mechanic_schema.jsonify(new_mechanic), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    """
    Get all mechanics
    ---
    tags:
      - Mechanics
    summary: Get mechanics
    description: Returns all mechanics.
    responses:
      200:
        description: List of mechanics
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: John Doe
              email:
                type: string
                example: john@email.com
              salary:
                type: number
                example: 60000
    """
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/top", methods=["GET"])
def top_mechanics():
    """
    Get top mechanics
    ---
    tags:
      - Mechanics
    summary: Get top mechanics
    description: Returns mechanics ranked by number of service tickets.
    responses:
      200:
        description: Ranked mechanics
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: John Doe
              ticket_count:
                type: integer
                example: 5
    """
    results = (
        db.session.query(
            Mechanic.id,
            Mechanic.name,
            func.count(service_mechanics.c.service_ticket_id).label("ticket_count")
        )
        .outerjoin(service_mechanics, Mechanic.id == service_mechanics.c.mechanic_id)
        .group_by(Mechanic.id, Mechanic.name)
        .order_by(func.count(service_mechanics.c.service_ticket_id).desc())
        .all()
    )

    return jsonify([
        {
            "id": mechanic_id,
            "name": name,
            "ticket_count": ticket_count
        }
        for mechanic_id, name, ticket_count in results
    ]), 200