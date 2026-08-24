"""Fruit Inventory REST API"""

from flask import Blueprint, jsonify

from bread.model import Inventory


blueprint = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@blueprint.route("/inventory", methods=["GET"])
def get_inventory():
    """Return all fruit inventory as JSON."""

    inventory = Inventory.select()

    inventory_list = []

    for item in inventory:
        inventory_list.append({
            "id": item.id,
            "fruit": item.fruit,
            "stock": item.stock,
            "expiration": item.expiration.strftime("%Y-%m-%d"),
            "location": item.location,
            "price": float(item.price)
        })

    return jsonify(inventory_list)