from flask import request, jsonify
from sqlalchemy import select, func
from marshmallow import ValidationError

from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from ...extensions import db
from ...models import Mechanic, service_mechanics


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
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
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/top", methods=["GET"])
def top_mechanics():
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