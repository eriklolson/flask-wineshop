from flask_wineshop.models import *
from flask_login import current_user


def get_cart(user_id):
    if current_user.is_authenticated:
        user_cart = Bottles.query.join(Stocks, Bottles.id == Stocks.bottles_id). \
            add_columns(Stocks.quantity). \
            join(Cart, Bottles.id == Cart.bottles_id). \
            add_columns(Bottles.id, Bottles.product_name, Bottles.color_name, Bottles.primary_grape,
                        Bottles.year, Bottles.image, Bottles.price, Cart.buy_quantity). \
            filter_by(buyer=current_user).all()
    else:
        user_cart = 0
    return user_cart


def get_quantity_total():
    if current_user.is_authenticated:
        quantity_total = 0
        user_id = current_user.id
        user_cart = get_cart(user_id)
        for bottle in user_cart:
            quantity_total += bottle.buy_quantity
    else:
        quantity_total = 0
    return quantity_total


def delete_from_cart(user_id, bottles_id):
    Cart.query.filter(Cart.bottles_id == bottles_id).filter(Cart.user_id == user_id).delete()
    db.session.commit()

