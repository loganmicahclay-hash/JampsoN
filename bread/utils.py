"""Utility functions"""

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

from bread.model import User, UserRoles, Roles

# This was modified from this article
# https://andypi.co.uk/2015/11/27/multiple-user-roles-python-flask/
def required_roles(*roles):
    """Decorator for requiring roles to view pages"""

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            user_roles = get_current_user_role()
            found = False
            for user_role in user_roles:
                if user_role in roles:
                    found = True
            if not found:
                flash(
                    "It appears you don't have permission to access that page!",
                    "error",
                )   
                return redirect(url_for("site.login"))
            return func(*args, **kwargs)

        return wrapped

    return wrapper


def get_current_user_role():
    """Get the roles for the current user"""

    user_roles = []

    if current_user.is_authenticated:
        roles = ( 
            User.select(User, Roles, UserRoles)
            .join(UserRoles)
            .join(Roles)
            .where(User.id == current_user.id)
        )   
        for role in roles:
            user_roles.append(role.userroles.role.name)

    return user_roles