from flask import Blueprint, render_template, request, redirect, url_for
from bread.model import User
import bcrypt

blueprint = Blueprint("customer", __name__)


@blueprint.route("/customers")
def customers():
    users = User.select()

    return render_template(
        "customer/customer.html",
        users=users
    )


@blueprint.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        password = request.form["password"].encode("utf-8")
        pass_hash = bcrypt.hashpw(password, bcrypt.gensalt())

        User.create(
            fname=request.form["fname"],
            lname=request.form["lname"],
            company_name=request.form["company_name"],
            address=request.form["address"],
            phone_number=request.form["phone_number"],
            email=request.form["email"],
            password=pass_hash
        )

        return redirect(url_for("customer.customers"))

    return render_template("customer/add.html")


@blueprint.route("/customers/<int:user_id>/edit", methods=["GET", "POST"])
def edit_customer(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None:
        return redirect(url_for("customer.customers"))

    if request.method == "POST":
        user.fname = request.form["fname"]
        user.lname = request.form["lname"]
        user.company_name = request.form["company_name"]
        user.address = request.form["address"]
        user.phone_number = request.form["phone_number"]
        user.email = request.form["email"]

        password = request.form["password"]

        if password:
            password = password.encode("utf-8")
            user.password = bcrypt.hashpw(
                password,
                bcrypt.gensalt()
            )

        user.save()

        return redirect(url_for("customer.customers"))

    return render_template(
        "customer/edit.html",
        user=user
    )


@blueprint.route("/customers/<int:user_id>/delete", methods=["GET", "POST"])
def delete_customer(user_id):
    user = User.get_or_none(User.id == user_id)

    if user is None:
        return redirect(url_for("customer.customers"))

    if request.method == "POST":
        user.delete_instance()

        return redirect(url_for("customer.customers"))

    return render_template(
        "customer/delete.html",
        user=user
    )