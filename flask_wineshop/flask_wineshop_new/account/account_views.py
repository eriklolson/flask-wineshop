from flask import render_template
from flask_login import login_required, current_user

from flask_wineshop.cart.helpers import get_quantity_total
from flask_wineshop.models import Bottles, Order, User, db, Cart, Countries, Stocks
from flask_wineshop.account import bp


@bp.route('/<username>/profile')
@login_required
def profile(username):
    """User profile page: shows account info"""
    quantity_total = get_quantity_total()
    user_id = current_user.id
    username = username
    return render_template('profile.jinja2', user_id=user_id, username=username, quantity_total=quantity_total)


@bp.route('/<username>/transactions')
@login_required
def transactions(username):
    """For displaying order history"""
    # user_id = current_user.id
    quantity_total = get_quantity_total()
    username = username
    orders = db.session.query(Order.id, Order.order_date, Order.order_total) \
        .filter(Order.user_id == current_user.id).all()
    return render_template('transactions.jinja2', username=username, orders=orders, quantity_total=quantity_total)
