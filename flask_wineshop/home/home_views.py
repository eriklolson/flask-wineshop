from flask import render_template
from flask_login import current_user

from . import bp
from flask_wineshop.models import Cart


@bp.route('/')
@bp.route('/index')
def index():
    """Homepage route."""
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
    quantity_total = Cart.get_quantity_total(current_user)
    return render_template(
        'index.jinja2', user_id=user_id, quantity_total=quantity_total)


