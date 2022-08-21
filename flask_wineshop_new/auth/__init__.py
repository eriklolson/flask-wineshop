from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
                'auth', __name__,
                template_folder='templates',
                static_folder='static'
)

from . import auth_views
