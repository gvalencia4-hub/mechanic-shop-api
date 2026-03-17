from flask import request, jsonify
from application.models import db, Inventory
from application.blueprints.inventory import inventory_bp


@inventory_bp.route("/", methods=["POST"])
def create_inventory():
    data = request.get_json()

    new_item = Inventory(
        name=data["name"],
        price=data["price"]
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Inventory item created",
        "inventory": {
            "id": new_item.id,
            "name": new_item.name,
            "price": new_item.price
        }
    }), 201


@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    items = Inventory.query.all()

    inventory_list = []
    for item in items:
        inventory_list.append({
            "id": item.id,
            "name": item.name,
            "price": item.price
        })

    return jsonify(inventory_list), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = Inventory.query.get_or_404(item_id)

    return jsonify({
        "id": item.id,
        "name": item.name,
        "price": item.price
    }), 200


@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_inventory(item_id):
    item = Inventory.query.get_or_404(item_id)
    data = request.get_json()

    item.name = data.get("name", item.name)
    item.price = data.get("price", item.price)

    db.session.commit()

    return jsonify({
        "message": "Inventory item updated",
        "inventory": {
            "id": item.id,
            "name": item.name,
            "price": item.price
        }
    }), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):
    item = Inventory.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Inventory item deleted"}), 200