from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
                'account', __name__,
                template_folder='templates',
                static_folder='static'
)

from . import account_views