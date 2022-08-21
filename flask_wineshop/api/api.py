from flask_wineshop.models import *
from flask import current_app as app
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields


#####################################################
# Create data abstraction layer
class BottleSchema(Schema):
    class Meta:
        type_ = 'bottle'
        self_view = 'bottle_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'bottle_list'

    id = fields.Integer(as_string=True)
    product_name = fields.Str()
    year = fields.Str()
    volume = fields.Str()
    proof = fields.Str()
    producer_name = fields.Str()
    country_id = fields.Integer()
    country_name = fields.Str()
    region_name = fields.Str()
    appellation = fields.Str()
    color_name = fields.Str()
    primary_grape = fields.Str()
    all_grape = fields.Str()
    price = fields.Str()
    image = fields.Str()
    description = fields.Str()


class CountrySchema(Schema):
    class Meta:
        type_ = 'country'
        self_view = 'country_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'country_list'

    id = fields.Integer(as_string=True)
    country_name = fields.Str()


class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'user_list'

    id = fields.Integer(as_string=True)
    username = fields.Str(required=True)
    email = fields.Email()
    # password = fields.Str()
    date_joined = fields.Str()
    last_login = fields.Str()
    cart = Relationship(self_view='user_cart',
                        self_view_kwargs={'id': '<id>'},
                        related_view='cart_one',
                        related_view_kwargs={'id': '<id>'},
                        schema='CartSchema',
                        type_='cart')


class CartSchema(Schema):
    class Meta:
        type_ = 'cart'
        self_view = 'cart_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'cart_list'

    id = fields.Integer(as_string=True)
    user_id = fields.Integer()
    bottles_id = fields.Integer()
    buy_quantity = fields.Integer()
    owner = Relationship(attribute='user',
                         self_view='cart_user',
                         self_view_kwargs={'id': '<id>'},
                         related_view='user_one',
                         related_view_kwargs={'cart_id': '<id>'},
                         schema='UserSchema',
                         type_='user')


#####################################################
# Create resource managers
#####################################################
class BottleList(ResourceList):
    schema = BottleSchema
    data_layer = {'session': db.session,
                  'model': Bottles}


class BottleOne(ResourceDetail):
    schema = BottleSchema
    data_layer = {'session': db.session,
                  'model': Bottles}


class CountryList(ResourceList):
    schema = CountrySchema
    data_layer = {'session': db.session,
                  'model': Countries}


class CountryOne(ResourceDetail):
    schema = CountrySchema
    data_layer = {'session': db.session,
                  'model': Countries}


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserOne(ResourceDetail):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserRelationship(ResourceRelationship):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class CartList(ResourceList):
    schema = CartSchema
    data_layer = {'session': db.session,
                  'model': Cart}


class CartOne(ResourceDetail):
    schema = CartSchema
    data_layer = {'session': db.session,
                  'model': Cart}


class CartRelationship(ResourceRelationship):
    schema = CartSchema
    data_layer = {'session': db.session,
                  'model': Cart}


#####################################################
# endpoints
#####################################################

api = Api(app)
api.route(BottleList, 'bottle_list', '/api/bottles')
api.route(BottleOne, 'bottle_one', '/api/bottles/<int:id>')
api.route(CountryList, 'country_list', '/api/countries')
api.route(CountryOne, 'country_one', '/api/countries/<int:id>')
api.route(UserList, 'user_list', '/api/users')
api.route(UserOne, 'user_one', '/api/users/<int:id>', '/carts/<int:cart_id>/owner')
api.route(UserRelationship, 'user_cart', '/api/users/<int:id>/relationships/carts')
api.route(CartList, 'cart_list', '/api/carts')
api.route(CartOne, 'cart_one', '/api/carts/<int:id>', '/users/<int:id>/carts')
api.route(CartRelationship, 'cart_user', '/api/carts/<int:id>/relationships/owner')
