"""
  This is the model for our database.  This is for peewee objects only.
"""

from datetime import datetime
from flask_login import UserMixin

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DecimalField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

db = SqliteDatabase("JampsoN.db")

class BaseModel(Model):
    """This is the base model so every model inherits the db connection"""

    class Meta:
        """Peewee Configuration"""

        database = db
        legacy_table_names = False


class User(UserMixin, BaseModel):
    """Store the users for this application"""

    id = AutoField(primary_key=True)
    fname = CharField()
    lname = CharField()
    company_name = CharField()
    address = CharField()
    phone_number = CharField(max_length=20)
    email = CharField()
    password = CharField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)


class Roles(BaseModel):
    """Roles table - permissions available to be assigned to users"""

    name = CharField(unique=True)
    description = CharField(null=True)


class UserRoles(BaseModel):
    """UserRoles table - The Roles assigned to users"""

    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref="roles")
    role = ForeignKeyField(Roles, backref="users")


class Locations(BaseModel):
    """Fruit Stand Locations"""

    id = AutoField(primary_key=True)
    name = CharField()
    address = CharField()
    employees = IntegerField()


class Inventory(BaseModel):
    """Tracks fruit crates and their inventory"""

    id = AutoField(primary_key=True)
    fruit = CharField()
    stock = IntegerField()
    expiration = DateTimeField()
    location = CharField()
    price = DecimalField(max_digits=10, decimal_places=2, default=0)


class Order(BaseModel):
    """Stores customer orders"""

    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref="orders")
    created_at = DateTimeField(default=datetime.now)
    status = CharField(default="confirmed")


class OrderItem(BaseModel):
    """Stores the individual fruits in an order"""

    id = AutoField(primary_key=True)
    order = ForeignKeyField(Order, backref="items")
    inventory = ForeignKeyField(Inventory, backref="order_items")
    quantity = IntegerField()