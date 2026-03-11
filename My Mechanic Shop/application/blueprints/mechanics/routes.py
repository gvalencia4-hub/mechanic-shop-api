from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from ...extensions import db
from ...models import Mechanic


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


@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)

        mechanic.name = mechanic_data["name"]
        mechanic.specialty = mechanic_data["specialty"]

        db.session.commit()

        return mechanic_schema.jsonify(mechanic), 200

    except ValidationError as err:
        return jsonify(err.messages), 400


@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic {id} deleted successfully"}), 200