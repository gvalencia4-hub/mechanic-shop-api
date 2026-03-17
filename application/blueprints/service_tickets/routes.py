from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from ...extensions import db
from ...models import ServiceTicket, Mechanic, Inventory
from ...decorators import token_required


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        new_ticket = service_ticket_schema.load(request.json)

        db.session.add(new_ticket)
        db.session.commit()

        return service_ticket_schema.jsonify(new_ticket), 201

    except ValidationError as err:
        return jsonify(err.messages), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this ticket"}), 200

    ticket.mechanics.append(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}"}), 200


@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket"}), 200

    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}"}), 200


@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    data = request.get_json() or {}
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    try:
        for mechanic_id in add_ids:
            mechanic = db.session.get(Mechanic, mechanic_id)
            if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

        for mechanic_id in remove_ids:
            mechanic = db.session.get(Mechanic, mechanic_id)
            if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

        db.session.commit()

        return jsonify({
            "message": f"Service ticket {ticket_id} updated successfully",
            "mechanic_ids": [m.id for m in ticket.mechanics]
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route("/<int:ticket_id>/add-part/<int:inventory_id>", methods=["POST"])
def add_part_to_ticket(ticket_id, inventory_id):
    try:
        ticket = ServiceTicket.query.get_or_404(ticket_id)
        item = Inventory.query.get_or_404(inventory_id)

        if item not in ticket.inventory_items:
            ticket.inventory_items.append(item)
            db.session.commit()

        return jsonify({"message": "Part added to service ticket"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200