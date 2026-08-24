"""HTMX Single Page App"""

from datetime import datetime

from flask import Flask, redirect, request, g
from flask_login import LoginManager, current_user
from peewee import DoesNotExist

from bread import site
from bread.model import db, User, Inventory
from bread.location import blueprint as location_blueprint
from bread.inventory import blueprint as inventory_blueprint
from bread.admin import blueprint as admin_blueprint
from bread.utils import get_current_user_role
from bread.customer import blueprint as customer_blueprint
from bread.order import blueprint as order_blueprint
from bread.api import blueprint as api_blueprint

app = Flask(__name__, static_folder="static", static_url_path="/static")

# App configuration ==========================================================
app.config["SECRET_KEY"] = "secret-developer-key"

# Flask Login =================================================================
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login load_user function"""

    user_calc_id = None

    try:
        user_calc_id = ( 
            User.select().where(User.id == user_id, User.active == True).get()  # noqa
        )   
    except IndexError as error:
        print(error)
    except DoesNotExist as error:
        print(error)

    return user_calc_id

# Database ====================================================================
@app.before_request
def setup_application():
    """Do the things we need to have an application."""

    db.connect()

    # Remove expired inventory
    Inventory.delete().where(
        Inventory.expiration <= datetime.now()
    ).execute()

    # Set the information about the user
    if not hasattr(g, "user"):
        g.user = current_user
        g.user_role = get_current_user_role()


@app.teardown_request
def close_db_connection(exc):
    """When the request stops let's politely stop the db connection (return it to the pool)"""

    if not db.is_closed():
        db.close()


# Blueprints ==================================================================
app.register_blueprint(site.blueprint)
app.register_blueprint(location_blueprint)
app.register_blueprint(inventory_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(api_blueprint)