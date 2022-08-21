from flask import Blueprint

# Blueprint Configuration
bp = Blueprint(
                'api', __name__,
                url_prefix='/api'
)

from . import api