"""Inventory Blueprint"""

from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from bread.model import Inventory
from bread.utils import required_roles


blueprint = Blueprint(
    "inventory",
    __name__,
    template_folder="templates",
    url_prefix="/inventory"
)


@blueprint.route("/")
@login_required
def browse():
    """The Browse mode for inventory"""

    remove_expired_inventory()

    inventory = Inventory.select().dicts()

    return render_template(
        "inventory/inventory.html",
        inventory=inventory
    )


@blueprint.route("/add")
@required_roles("admin")
def add():
    """The Add mode"""

    min_expiration = datetime.now() + timedelta(days=1)

    min_expiration = min_expiration.replace(
        second=0,
        microsecond=0
    )

    return render_template(
        "inventory/add.html",
        min_expiration=min_expiration.strftime("%Y-%m-%dT%H:%M")
    )


@blueprint.route("/save", methods=["POST"])
@required_roles("admin")
def save():
    """Save a new crate"""

    fruit = request.form.get("fruit")
    stock = request.form.get("stock")
    price = request.form.get("price")
    expiration = request.form.get("expiration")
    location = request.form.get("location")

    expiration = datetime.strptime(
        expiration,
        "%Y-%m-%dT%H:%M"
    )

    if expiration < datetime.now() + timedelta(days=1):
        return "Expiration date must be at least 1 day in the future.", 400

    Inventory.create(
        fruit=fruit,
        stock=stock,
        price=price,
        expiration=expiration,
        location=location
    )

    return redirect(url_for("inventory.browse"))


@blueprint.route("/update/<int:inventory_id>", methods=["POST"])
@required_roles("admin")
def update(inventory_id):
    """Update an existing crate"""

    inventory = Inventory.get_by_id(inventory_id)

    inventory.fruit = request.form.get("fruit")
    inventory.stock = request.form.get("stock")
    inventory.price = request.form.get("price")
    inventory.location = request.form.get("location")

    # Get the new expiration date/time
    expiration = request.form.get("expiration")

    # Convert it from the form format to a Python datetime
    expiration = datetime.strptime(
        expiration,
        "%Y-%m-%dT%H:%M"
    )

    # Expiration must be at least 1 day in the future
    if expiration < datetime.now() + timedelta(days=1):
        return "Expiration date must be at least 1 day in the future.", 400

    inventory.expiration = expiration

    inventory.save()

    return redirect(url_for("inventory.browse"))


@blueprint.route("/edit/<int:inventory_id>")
@required_roles("admin")
def edit(inventory_id):
    """Edit an existing crate"""

    inventory = Inventory.get_by_id(inventory_id)

    min_expiration = datetime.now() + timedelta(days=1)

    min_expiration = min_expiration.replace(
        second=0,
        microsecond=0
    )

    return render_template(
        "inventory/edit.html",
        inventory=inventory,
        min_expiration=min_expiration.strftime("%Y-%m-%dT%H:%M")
    )


@blueprint.route("/delete/<int:inventory_id>")
@required_roles("admin")
def delete(inventory_id):
    """Confirm deletion of a crate"""

    inventory = Inventory.get_by_id(inventory_id)

    return render_template(
        "inventory/delete.html",
        inventory=inventory
    )


@blueprint.route("/delete/<int:inventory_id>/confirm", methods=["POST"])
@required_roles("admin")
def delete_confirm(inventory_id):
    """Delete the crate"""

    inventory = Inventory.get_by_id(inventory_id)

    inventory.delete_instance()

    return redirect(url_for("inventory.browse"))

def remove_expired_inventory():
    """Delete inventory that has passed its expiration date."""

    expired_inventory = Inventory.delete().where(
        Inventory.expiration <= datetime.now()
    )

    deleted = expired_inventory.execute()

    return deleted