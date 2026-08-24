# Python module imports

import bcrypt

from flask import (
    Blueprint,
    render_template,
    g,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, login_user, logout_user
from peewee import DoesNotExist

# Local imports
from bread.model import User, Locations


blueprint = Blueprint(
    "site",
    __name__,
    template_folder="templates",
    url_prefix="/"
)


# ==========================================================
# HOME PAGE
# ==========================================================

@blueprint.route("/")
def index():
    """The Index Page for this site."""

    locations = Locations.select()

    return render_template(
        "site/index.html",
        locations=locations
    )


# ==========================================================
# LOGIN
# ==========================================================

@blueprint.route("/login")
def login():
    """Display the login page."""

    return render_template("site/login.html")


@blueprint.route("/login", methods=["POST"])
def login_post():
    """Perform the login."""

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Find the active user by email
        current_user = User.get(
            (User.email == email) &
            (User.active == True)
        )

        # Check the password
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            current_user.password.encode("utf-8")
        ):
            flash("Please verify your login details and try again.")

            return redirect(url_for("site.login"))

    except DoesNotExist:

        flash("Please verify your login details and try again.")

        return redirect(url_for("site.login"))

    else:

        # Log the user into Flask-Login
        login_user(current_user)

        # Store the actual User object
        g.user = current_user

    return redirect(url_for("site.index"))


# ==========================================================
# SIGN UP
# ==========================================================

@blueprint.route("/signup")
def signup():
    """Display the sign-up page."""

    return render_template("site/signup.html")


@blueprint.route("/signup", methods=["POST"])
def signup_post():
    """Create a new user account."""

    # Get information from the form
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    company_name = request.form.get("company_name")
    address = request.form.get("address")
    phone_number = request.form.get("phone_number")
    email = request.form.get("email")
    password = request.form.get("password")

    # Make company name blank instead of None
    if not company_name:
        company_name = ""

    # Check if the email is already registered
    existing_user = User.get_or_none(
        User.email == email
    )

    if existing_user:
        flash("An account with that email already exists.")

        return redirect(url_for("site.signup"))

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Create the new user
    user = User.create(
        fname=fname,
        lname=lname,
        company_name=company_name,
        address=address,
        phone_number=phone_number,
        email=email,
        password=hashed_password,
        active=True
    )

    # Log the new user in immediately
    login_user(user)

    return redirect(url_for("site.index"))


# ==========================================================
# LOGOUT
# ==========================================================

@blueprint.route("/logout")
@login_required
def logout():
    """Logout the user."""

    logout_user()

    return redirect(url_for("site.index"))