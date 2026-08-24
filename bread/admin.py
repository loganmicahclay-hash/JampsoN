from flask import Blueprint, render_template
from bread.utils import required_roles

blueprint = Blueprint("admin",
__name__,
template_folder="templates",
url_prefix="/admin"
)


@blueprint.route("/")
@required_roles("admin")
def index():
    """The admin Page for this site"""

    return render_template("admin/admin_index.html")