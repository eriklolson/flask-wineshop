from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
        'home', __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/home/static'
)

from . import home_views
