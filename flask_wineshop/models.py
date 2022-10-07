"""Models"""
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import flash
from flask_login import UserMixin, current_user
from . import db
import json


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    date_joined = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    cart = db.relationship('Cart', back_populates='buyer', lazy='joined')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_orders(user_id):
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.id).all()
        return orders

    def save_user_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, user_id):
        return User.query.filter_by(id=user_id).first()

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Cart(UserMixin, db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), nullable=True)
    buy_quantity = db.Column(db.Integer, nullable=True, default=1)

    buyer = db.relationship('User', back_populates='cart', lazy='joined')
    items = db.relationship('Bottles', back_populates='cart', lazy='joined')

    def __init__(self, user_id, bottles_id, buy_quantity):
        self.user_id = user_id
        self.bottles_id = bottles_id
        self.buy_quantity = buy_quantity

    def __repr__(self):
        return f"Cart('{self.id}', '{self.bottles_id}, '{self.user_id}', '{self.buy_quantity}'))"

    def get_cart(user_id):
        if current_user.is_authenticated:
            cart = Bottles.query.join(Stocks, Bottles.id == Stocks.bottles_id). \
                add_columns(Stocks.quantity). \
                join(Cart, Bottles.id == Cart.bottles_id). \
                add_columns(Bottles.id, Bottles.product_name, Bottles.color_name, Bottles.primary_grape,
                            Bottles.year, Bottles.image, Bottles.price, Cart.buy_quantity). \
                filter_by(buyer=current_user).all()
        else:
            cart = 0
        return cart

    def add_to_cart(user_id, bottles_id, buy_quantity):
        item_to_add = Cart(user_id=user_id, bottles_id=bottles_id, buy_quantity=buy_quantity)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Product added to cart', 'success')

    def delete_from_cart(user_id, bottles_id):
        Cart.query.filter(Cart.bottles_id == bottles_id).filter(Cart.user_id == user_id).delete()
        db.session.commit()
        flash('Product deleted from cart', 'success')

    def get_quantity_total(current_user):
        if current_user.is_authenticated:
            quantity_total = 0
            user_id = current_user.id
            user_cart = Cart.get_cart(user_id=user_id)
            for bottle in user_cart:
                quantity_total += bottle.buy_quantity
        else:
            quantity_total = 0
        return quantity_total

    def cart_order(user_id, order_total):
        items = db.session.query(Cart).filter(Cart.user_id == user_id).all()
        for item in items:
            order = Order(user_id=item.user_id, order_date=datetime.utcnow(), order_total=order_total)
            db.session.add(order)
            db.session.commit()

    def remove_ordered_items_from_cart(user_id):
        db.session.query(Cart).filter(Cart.user_id == user_id).delete()
        db.session.commit()

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Order(UserMixin, db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    order_total = db.Column(db.DECIMAL, nullable=False)

    def __init__(self, user_id, order_date, order_total):
        self.user_id = user_id
        self.order_date = order_date
        self.order_total = order_total

    def __repr__(self):
        return f"Order('{self.id}', '{self.user_id}','{self.order_date}','{self.order_total}')"

    def get_order_id(user_id):
        order_id = db.session.query(Order.id).filter(Order.user_id == user_id).order_by(Order.id.desc()).first()
        order_id = order_id[0]
        return order_id

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class OrderedItems(UserMixin, db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)

    def __init__(self, order_id, bottles_id, quantity):
        self.order_id = order_id
        self.bottles_id = bottles_id
        self.quantity = quantity

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.bottles_id}','{self.quantity}', '{self.item_price}')"

    def update_ordered_items(user_id, order_id):
        cart = Cart.query.with_entities(Cart.bottles_id, Cart.buy_quantity).filter(Cart.user_id == user_id)
        for item in cart:
            ordered_cart_item = OrderedItems(order_id=order_id, bottles_id=item.bottles_id, quantity=item.buy_quantity)
            db.session.add(ordered_cart_item)
            db.session.commit()

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Transactions(UserMixin, db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'), nullable=False)
    transaction_date = db.Column(db.DateTime,nullable=False)
    transaction_total = db.Column(db.DECIMAL, nullable=False)
    card_number = db.Column(db.String(50), nullable=False)
    card_type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(50), nullable=True)

    def __init__(self, order_id, transaction_date, transaction_total, card_number, card_type, response):
        self.order_id = order_id
        self.transaction_date = transaction_date
        self.transaction_total = transaction_total
        self.card_number = card_number
        self.card_type = card_type
        self.response = response

    def __repr__(self):
        return f"Order('{self.id}', '{self.order_id}','{self.transaction_date}','{self.transaction_total}'," \
               f"'{self.card_number}'), '{self.card_type}', '{self.response}')"

    def update_transactions(order_id, order_date, order_total, card_number, card_type):
        transaction = Transactions(order_id=order_id, transaction_date=order_date, transaction_total=order_total,
                                   card_number=card_number, card_type=card_type, response='success')
        db.session.add(transaction)
        db.session.commit()

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Bottles(UserMixin, db.Model):
    __tablename__ = 'bottles'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(120), nullable=False)
    volume = db.Column(db.String(120), nullable=False)
    proof = db.Column(db.String(120), nullable=False)
    producer_name = db.Column(db.String(120), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country_name = db.Column(db.String(120), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    region_name = db.Column(db.String(120), nullable=False)
    appellation = db.Column(db.String(120), nullable=False)
    color_name = db.Column(db.String(120), nullable=False)
    primary_grape = db.Column(db.String(120), nullable=False)
    all_grape = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    countries = db.relationship('Countries', back_populates='bottles')
    regions = db.relationship('Regions', back_populates='bottles')
    inventory = db.relationship('Stocks', back_populates='bottle', lazy='joined', uselist=False)
    cart = db.relationship('Cart', back_populates='items', lazy='joined')

    def __init__(self, product_name, year, volume, proof, producer_name, region_name, appellation, color_name,
                 primary_grape, all_grape, price, image, description):
        self.product_name = product_name
        self.year = year
        self.volume = volume
        self.proof = proof
        self.producer_name = producer_name
        self.region_name = region_name
        self.appellation = appellation
        self.color_name = color_name
        self.primary_grape = primary_grape
        self.all_grape = all_grape
        self.price = price
        self.year = year
        self.image = image
        self.description = description

    def __repr__(self):
        return '<Bottles {}>'.format(self.product_name)

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Stocks(UserMixin, db.Model):
    __tablename__ = 'stocks'
    bottles_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    bottle = db.relationship('Bottles', back_populates='inventory', lazy='joined')

    def __init__(self, bottles_id, quantity):
        self.bottles_id = bottles_id
        self.quantity = quantity

    def __repr__(self):
        return '<Stocks {}>'.format(self.quantity)

    def is_available(bottles_id):
        result = db.session.query(Stocks.quantity, Stocks.bottles_id).filter(Bottles.id == bottles_id).filter(
            Bottles.id == Stocks.bottles_id).first()
        return result

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Countries(UserMixin, db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(120), unique=True, nullable=False)

    bottles = db.relationship('Bottles', back_populates='countries')

    def __init__(self, country_name):
        self.country_name = country_name

    def __repr__(self):
        return '<Countries {}>'.format(self.country_name)

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)


class Regions(UserMixin, db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(120), unique=True, nullable=False)

    bottles = db.relationship('Bottles', back_populates='regions')

    def __init__(self, region_name):
        self.region_name = region_name

    def __repr__(self):
        return '<Regions {}>'.format(self.region_name)

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, sort_keys=True)