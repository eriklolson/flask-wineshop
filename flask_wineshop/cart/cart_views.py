"""Routes for shopping cart and order"""
from flask import abort, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from flask_wineshop.extensions import db
from .forms import *
from flask_wineshop.models import Cart, OrderedItems, Transactions, Stocks, Order
from flask_wineshop.cart import bp


@bp.route('/cart/<int:user_id>', methods=['GET', 'POST'])
@login_required
def cart(user_id):
    if current_user.id != user_id:
        return abort(403)
    else:
        user_cart = Cart.get_cart(user_id=current_user.id)
        grand_total = 0
        quantity_total = Cart.get_quantity_total(current_user)
        for bottle in user_cart:
            grand_total += float(bottle.price) * int(bottle.buy_quantity)

        if request.method == 'POST':
            bottles_id = request.form.get('bottle.id')
            quantity = request.form.get('qty')
            cart_item = db.session.query(Cart).filter_by(bottles_id=bottles_id).first()
            cart_item.buy_quantity = quantity
            db.session.commit()
            grand_total = 0
            for item in user_cart:
                grand_total += float(item.price) * int(item.buy_quantity)
    return render_template('cart.jinja2', title="Shopping Cart", user_cart=user_cart,
                           quantity_total=quantity_total, grand_total=grand_total)


@bp.route('/cart/add <int:bottles_id>', methods=['POST'])
@login_required
def add_to_cart(bottles_id):
    quantity = request.form.get('qty')
    user_cart = Cart.get_cart(user_id=current_user.id)
    # check if bottle in cart
    if bottles_id in user_cart:
        # if yes, update quantity
        item = db.session.query(Cart).filter_by(bottles_id=bottles_id, buyer=current_user).first()
        item.buy_quantity += 1
        db.session.commit()
        flash('This product already in cart, quantity added!' 'error')
    else:
        Cart.add_to_cart(current_user.id, bottles_id, quantity)
    return redirect(url_for('cart.cart', user_id=current_user.id))


@bp.route('/cart/update <int:bottles_id>', methods=['POST'])
@login_required
def update_cart(bottles_id):
    # Update quantity of a product in cart
    item = db.session.query(Cart).filter_by(bottles_id=bottles_id, buyer=current_user).first()
    item.buy_quantity = int(request.form.get('qty'))
    db.session.commit()
    return redirect(url_for('cart.cart', user_id=current_user.id))


@bp.route('/cart/remove <int:bottles_id>')
@login_required
def remove_from_cart(bottles_id):
    Cart.delete_from_cart(user_id=current_user.id, bottles_id=bottles_id)
    return redirect(url_for('cart.cart', user_id=current_user.id))


@bp.route('/order/<order_total>', methods=['GET', 'POST'])
@login_required
def create_order(order_total):
    form = CheckoutForm
    user_id = current_user.id
    quantity_total = 0
    user_cart = Cart.get_cart(user_id=user_id)
    fullname = request.form.get('fullname')
    order_date = datetime.utcnow()
    for item in user_cart:
        if item.buy_quantity > item.quantity:
            flash('not enough in stock', 'error')
        else:
            stock_item = db.session.query(Stocks).filter(Stocks.bottles_id == item.id).first()
            stock_item.quantity = item.quantity - item.buy_quantity
            db.session.add(stock_item)
            db.session.flush()
            db.session.commit()
    order_id = db.session.query(Order.id).filter(Order.user_id == user_id)
    order_id.order_by(Order.id.desc()).first()
    card_number = request.form.get('card_number')
    card_type = request.form.get('card_type')
    order = Order(user_id=user_id, order_date=order_date, order_total=order_total)
    db.session.add(order)
    db.session.flush()
    db.session.commit()
    order_id = Order.get_order_id(user_id)
    OrderedItems.update_ordered_items(user_id, order_id)
    Transactions.update_transactions(order_id, order_date, order_total, card_number, card_type)
    Cart.remove_ordered_items_from_cart(user_id)

    return render_template('ordered.jinja2', fullname=fullname, order_id=order_id, order_total=order_total, form=form,
                           quantity_total=quantity_total)
