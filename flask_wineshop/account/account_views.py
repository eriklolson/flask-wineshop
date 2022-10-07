from flask import render_template
from flask_login import login_required, current_user

from flask_wineshop.models import db, Order, Cart
from flask_wineshop.account import bp


@bp.route('/<username>/profile')
@login_required
def profile(username):
    """User profile page: shows account info"""
    user_id = current_user.id
    quantity_total = Cart.get_quantity_total(current_user)
    username = username
    return render_template('profile.jinja2', user_id=user_id, username=username, quantity_total=quantity_total)


@bp.route('/<username>/transactions')
@login_required
def transactions(username):
    """For displaying order history"""
    # user_id = current_user.id
    quantity_total = Cart.get_quantity_total(current_user)
    username = username
    orders = db.session.query(Order.id, Order.order_date, Order.order_total) \
        .filter(Order.user_id == current_user.id).all()
    return render_template('transactions.jinja2', username=username, orders=orders, quantity_total=quantity_total)
