#!/usr/bin/env python3

import bcrypt

# Python standard imports
from datetime import datetime, timedelta

# Import the tables and database connection
from bread.model import db, Locations, Inventory, Roles, User, UserRoles


# Let the user know what is going on
print("Seeding the database")


# Connect to the database
db.connect()


# Roles -----------------------------------------------------------------------
print(" - Creating Roles...", end="")

Roles.create(
    name="admin",
    description="The administrator"
)

print(" done")


# Users -----------------------------------------------------------------------
print(" - Creating Users...", end="")


# Logan
password = "baz".encode("utf-8")
pass_hash = bcrypt.hashpw(password, bcrypt.gensalt())

User.create(
    fname="Logan",
    lname="Clay",
    company_name="",
    address="421 Bluebonnet Ridge Dr Austin, TX 78745 USA",
    phone_number="123-456-7890",
    email="logan.clay@example.com",
    password=pass_hash
)


# Caleb
password = "secret123".encode("utf-8")
pass_hash = bcrypt.hashpw(password, bcrypt.gensalt())

User.create(
    fname="Caleb",
    lname="Johnson",
    company_name="",
    address="1458 Oak Street Denver, CO 80203 USA",
    phone_number="303-555-7812",
    email="caleb.johnson@example.com",
    password=pass_hash
)


# Admin User
password = "admin".encode("utf-8")
pass_hash = bcrypt.hashpw(password, bcrypt.gensalt())

admin = User.create(
    fname="Admin",
    lname="bar",
    company_name="",
    address="unknown",
    phone_number="000-000-0000",
    email="admin@bar.com",
    password=pass_hash
)


print(" done")


# User Roles ------------------------------------------------------------------
print(" - Creating User Roles...", end="")

UserRoles.create(
    user=admin.id,
    role=1
)

print(" done")


# Locations -------------------------------------------------------------------
print(" - Creating Locations...", end="")

Locations.create(
    name="Logan",
    address="7421 Bluebonnet Ridge Dr Austin, TX 78745 USA",
    employees=25
)

Locations.create(
    name="Dave",
    address="Calle Los Almendros #47 Santiago de los Caballeros, Santiago Dominican Republic",
    employees=10
)

Locations.create(
    name="Caleb",
    address="Av. Los Jardines #128 Santo Domingo, Distrito Nacional Dominican Republic",
    employees=-67
)

print(" done")


# Inventory -------------------------------------------------------------------
print(" - Creating Inventory...", end="")

Inventory.create(
    fruit="Apple",
    stock=50,
    expiration=datetime.now() + timedelta(days=7),
    location="Texas",
    price=1.25
)

Inventory.create(
    fruit="Banana",
    stock=30,
    expiration=datetime.now() + timedelta(days=5),
    location="Texas",
    price=0.75
)

Inventory.create(
    fruit="Orange",
    stock=45,
    expiration=datetime.now() + timedelta(days=10),
    location="Texas",
    price=1.00
)

Inventory.create(
    fruit="Mango",
    stock=53,
    expiration=datetime.now() + timedelta(days=3),
    location="Texas",
    price=0.50
)

Inventory.create(
    fruit="Grape",
    stock=37,
    expiration=datetime.now() + timedelta(days=12),
    location="Texas",
    price=2.50
)

Inventory.create(
    fruit="Strawberry",
    stock=25,
    expiration=datetime.now() + timedelta(days=4),
    location="Texas",
    price=3.00
)

Inventory.create(
    fruit="Apple",
    stock=42,
    expiration=datetime.now() + timedelta(days=14),
    location="Santiago",
    price=1.50
)

Inventory.create(
    fruit="Banana",
    stock=60,
    expiration=datetime.now() + timedelta(days=6),
    location="Santiago",
    price=0.65
)

Inventory.create(
    fruit="Orange",
    stock=35,
    expiration=datetime.now() + timedelta(days=9),
    location="Santiago",
    price=1.10
)

Inventory.create(
    fruit="Mango",
    stock=48,
    expiration=datetime.now() + timedelta(days=5),
    location="Santiago",
    price=0.85
)

print(" done")


# Close the database connection
db.close()