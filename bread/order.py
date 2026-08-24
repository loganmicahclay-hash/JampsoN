"""Order Blueprint"""

from flask import Blueprint, render_template, session, redirect, url_for, g, make_response

from bread.model import Inventory, Order, OrderItem


blueprint = Blueprint(
    "order",
    __name__,
    template_folder="templates",
    url_prefix="/order"
)


@blueprint.route("/fruit")
def fruit():
    """Fruit ordering page"""

    # Start a completely new order
    session.pop("cart", None)

    inventory = Inventory.select()

    cart = {}

    return render_template(
        "order/fruit.html",
        inventory=inventory,
        cart=cart
    )


@blueprint.route("/crate")
def crate():
    """Crate ordering page"""

    session.pop("crate_cart", None)

    inventory = Inventory.select()

    cart = {}

    return render_template(
        "order/crate.html",
        inventory=inventory,
        cart=cart
    )


@blueprint.route("/add/<int:inventory_id>", methods=["POST"])
def add_to_order(inventory_id):
    """Add one fruit to the temporary order"""

    inventory = Inventory.get_by_id(inventory_id)

    cart = session.get("cart", {})

    item_id = str(inventory_id)

    current_quantity = cart.get(item_id, 0)

    # Check available stock
    if current_quantity >= inventory.stock:
        return """
            <div class="alert alert-warning">
                Sorry, this fruit is out of stock.
            </div>
        """

    # Add one fruit to cart
    cart[item_id] = current_quantity + 1

    session["cart"] = cart

    # Build order display
    order_items = []

    for item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price
        })

    # Calculate temporary stock
    remaining_stock = inventory.stock - cart[str(inventory_id)]

    # Calculate total price of everything in cart
    total_price = sum(
        item["price"] * item["quantity"]
        for item in order_items
    )

    return render_template(
        "order/order_items.html",
        order_items=order_items,
        inventory=inventory,
        remaining_stock=remaining_stock,
        total_price=total_price
    )


@blueprint.route("/crate/add/<int:inventory_id>", methods=["POST"])
def add_crate_to_order(inventory_id):

    inventory = Inventory.get_by_id(inventory_id)

    cart = session.get("crate_cart", {})

    item_id = str(inventory_id)

    if item_id in cart:
        return ""

    cart[item_id] = inventory.stock

    session["crate_cart"] = cart

    order_items = []

    for cart_item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(cart_item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price,
            "crate_price": item.price * quantity
        })

    total_price = sum(
        item["crate_price"]
        for item in order_items
    )

    return render_template(
        "order/crate_items.html",
        order_items=order_items,
        total_price=total_price
    )


@blueprint.route("/remove/<int:inventory_id>", methods=["POST"])
def remove_from_order(inventory_id):
    """Remove one fruit from the temporary order."""

    cart = session.get("cart", {})

    item_id = str(inventory_id)

    # Check if this fruit is actually in the cart
    if item_id in cart:

        # Remove one from the quantity
        cart[item_id] -= 1

        # If quantity reaches zero, remove it completely
        if cart[item_id] <= 0:
            del cart[item_id]

    # Save the updated cart
    session["cart"] = cart

    # Build the updated order display
    order_items = []

    for item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price
        })

    inventory = Inventory.get_by_id(inventory_id)

    remaining_stock = inventory.stock - cart.get(str(inventory_id), 0)

    total_price = sum(
        item["price"] * item["quantity"]
        for item in order_items
    )

    return render_template(
        "order/order_items.html",
        order_items=order_items,
        inventory=inventory,
        remaining_stock=remaining_stock,
        total_price=total_price
    )


@blueprint.route("/crate/remove/<int:inventory_id>", methods=["POST"])
def remove_crate_from_order(inventory_id):

    cart = session.get("crate_cart", {})

    item_id = str(inventory_id)

    cart.pop(item_id, None)

    session["crate_cart"] = cart

    order_items = []

    for cart_item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(cart_item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price
        })

    removed_crate = Inventory.get_by_id(inventory_id)

    return (
        render_template(
            "order/crate_items.html",
            order_items=order_items
        )
        +
        render_template(
            "order/crate_button.html",
            item=removed_crate
        )
    )


@blueprint.route("/checkout")
def checkout():
    """Show the final order confirmation page."""

    cart = session.get("cart", {})

    if not cart:
        return redirect(url_for("order.fruit"))

    order_items = []

    for item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price
        })

    total_price = sum(
        item["price"] * item["quantity"]
        for item in order_items
    )

    return render_template(
        "order/checkout.html",
        order_items=order_items,
        total_price=total_price,
        user=g.user
    )


@blueprint.route("/crate/checkout")
def crate_checkout():
    """Show the final crate order confirmation page."""

    cart = session.get("crate_cart", {})

    if not cart:
        return redirect(url_for("order.crate"))

    order_items = []

    for item_id, quantity in cart.items():

        item = Inventory.get_by_id(int(item_id))

        order_items.append({
            "id": item.id,
            "fruit": item.fruit,
            "quantity": quantity,
            "location": item.location,
            "price": item.price,
            "crate_price": item.price * quantity
        })

    total_price = sum(
        item["crate_price"]
        for item in order_items
    )

    return render_template(
        "order/crate_checkout.html",
        order_items=order_items,
        total_price=total_price,
        user=g.user
    )


@blueprint.route("/confirm", methods=["POST"])
def confirm_order():
    """Permanently save the order."""

    cart = session.get("cart", {})

    # Make sure there is actually an order
    if not cart:
        return redirect(url_for("order.fruit"))

    # Create the order
    order = Order.create(
        user=g.user,
        status="confirmed"
    )

    # Process every item in the cart
    for item_id, quantity in cart.items():

        inventory = Inventory.get_by_id(int(item_id))

        # Double-check that enough stock is available
        if quantity > inventory.stock:
            return "Sorry, there is not enough stock available."

        # Save the item in the order
        OrderItem.create(
            order=order,
            inventory=inventory,
            quantity=quantity
        )

        # Permanently decrease inventory
        inventory.stock -= quantity
        inventory.save()

    # Order is complete, so clear the temporary cart
    session.pop("cart", None)

    return render_template(
        "order/order_confirmed.html",
        order=order
    )


@blueprint.route("/crate/confirm", methods=["POST"])
def confirm_crate_order():

    cart = session.get("crate_cart", {})

    if not cart:
        return redirect(url_for("order.crate"))

    order = Order.create(
        user=g.user,
        status="confirmed"
    )

    for item_id, quantity in cart.items():

        inventory = Inventory.get_by_id(int(item_id))

        OrderItem.create(
            order=order,
            inventory=inventory,
            quantity=quantity
        )

        # Empty the crate
        inventory.stock = 0
        inventory.save()

    session.pop("crate_cart", None)

    return render_template(
        "order/order_confirmed.html",
        order=order
    )


@blueprint.route("/crate/reset", methods=["POST"])
def reset_crate_order():
    """Completely reset the temporary crate order."""

    session.pop("crate_cart", None)

    return redirect(url_for("order.crate"))