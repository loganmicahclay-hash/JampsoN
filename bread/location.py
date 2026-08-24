"""Location Blueprint"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from bread.model import Locations
from bread.utils import required_roles

blueprint = Blueprint(
    "location",
    __name__,
    template_folder="templates",
    url_prefix="/location"
)


@blueprint.route("/")
@login_required
def browse():
    """The Browse mode for location"""

    location = Locations.select().dicts()

    return render_template(
        "location/location.html",
        location=location
    )


@blueprint.route("/add")
def add():
    """The Add mode"""

    return render_template("location/add.html")


@blueprint.route("/save", methods=["POST"])
def save():
    """Save a new location"""

    # Capture the user's input from the form
    manager = request.form.get("manager")
    address = request.form.get("address")
    employees = request.form.get("employees")

    # Save the input to the database
    Locations.create(
        name=manager,
        address=address,
        employees=employees
    )

    # Return to the browse screen
    return redirect(url_for("location.browse"))


@blueprint.route("/update/<int:location_id>", methods=["POST"])
@required_roles("admin")
def update(location_id):
    """Update an existing location"""

    location = Locations.get_by_id(location_id)

    location.name = request.form.get("manager")
    location.address = request.form.get("address")
    location.employees = request.form.get("employees")

    location.save()

    return redirect(url_for("location.browse"))


@blueprint.route("/edit/<int:location_id>")
@required_roles("admin")
def edit(location_id):
    """Edit an existing location"""

    location = Locations.get_by_id(location_id)

    return render_template(
        "location/edit.html",
        location=location
    )


@blueprint.route("/delete/<int:location_id>")
@required_roles("admin")
def delete(location_id):
    """Confirm deletion of a location"""

    location = Locations.get_by_id(location_id)

    return render_template(
        "location/delete.html",
        location=location
    )


@blueprint.route("/delete/<int:location_id>/confirm", methods=["POST"])
@required_roles("admin")
def delete_confirm(location_id):
    """Delete the location"""

    location = Locations.get_by_id(location_id)

    location.delete_instance()

    return redirect(url_for("location.browse"))