from flask import request, current_app as app, Blueprint, render_template, session, g
# from flask_login import current_user
from . import bp
from flask_wineshop.cart.helpers import get_quantity_total, current_user
import requests
import json


"""Extract nested values from a JSON tree."""
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


@bp.route('/')
@bp.route('/index')
def index():
    """Homepage route."""
    quantity_total = get_quantity_total()
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
    return render_template(
        'index.jinja2', user_id=user_id, quantity_total=quantity_total)
