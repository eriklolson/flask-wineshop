from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
                'auth', __name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/auth/static'
)

from . import auth_views
