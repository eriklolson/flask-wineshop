from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField,  SubmitField, RadioField
from wtforms.validators import DataRequired, Length

from flask_wineshop.models import *


# FlaskForm for checkout details
class CheckoutForm(FlaskForm):
    fullname = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    card_type = RadioField('card_type')
    card_number = StringField('Credit card number',
                           validators=[DataRequired(), Length(min=12, max=12)])
    expdate = StringField('Exp Date',
                           validators=[DataRequired(), Length(min=4, max=4)])
    cvv = StringField('CVV',
                      validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Checkout')


class UpdateCartForm(FlaskForm):
    quantity = IntegerField('Quantity: ', default=1)


# Adds data to OrderedItems table
def update_ordered_items(order_id, user_id):
    cart = Cart.query.with_entities(Cart.bottles_id, Cart.buy_quantity).filter(Cart.user_id == user_id)
    for item in cart:
        ordered_cart_item = OrderedItems(order_id=order_id, bottles_id=item.bottles_id, quantity=item.buy_quantity)
        db.session.add(ordered_cart_item)
        db.session.commit()


# Removes sold products from user's cart
def remove_ordered_items_from_cart(user_id):
    db.session.query(Cart).filter(Cart.user_id == user_id).delete()
    db.session.commit()


# Updates the Transactions table for record of transactions
def update_transactions(order_id, order_date, order_total, card_number, card_type):
    transaction = Transactions(order_id=order_id, transaction_date=order_date, transaction_total=order_total,
                                       card_number=card_number, card_type=card_type, response='success')
    db.session.add(transaction)
    db.session.flush()
    db.session.commit()
