#!/usr/bin/env python3

import os
from urllib.parse import quote as url_quote

# Bread Project Libraries
from bread.model import db, Locations, Inventory, Roles, User, UserRoles, Order, OrderItem

if os.path.isfile("JampsoN.db"):
    os.remove("JampsoN.db")

# Talk to the user
print("Initializing the Database")

# =============================================================================
# Connect to the database
db.connect()

# Create the tables
print("  - Creating tables...", end="")
db.create_tables([Locations, Inventory, Roles, User, UserRoles, Order, OrderItem])
print(" done")

# Close the database connection
db.close()