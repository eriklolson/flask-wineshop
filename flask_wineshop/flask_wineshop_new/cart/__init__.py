from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
        'cart', __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/cart/static'
)

from . import cart_views