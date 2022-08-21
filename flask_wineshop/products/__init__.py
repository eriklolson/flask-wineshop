from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
        'products', __name__,
        template_folder='templates',
        static_folder='static'
)

from . import products_views