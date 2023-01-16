from os import environ
from flask import Flask
from flask_assets import Environment

from config import config
from .extensions import db, login_manager, migrate


def create_app(config_name=None):
    if config_name is None:
        config_name = environ.get('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    assets = Environment()
    assets.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # import parts of application
        from flask_wineshop.assets import compile_static_assets

        from .account import bp as account_bp
        app.register_blueprint(account_bp)

        from .auth import bp as auth_bp
        app.register_blueprint(auth_bp)

        from .cart import bp as cart_bp
        app.register_blueprint(cart_bp)

        from .home import bp as home_bp
        app.register_blueprint(home_bp)

        from .products import bp as products_bp
        app.register_blueprint(products_bp)

        # create Database Models
        db.create_all()
        compile_static_assets(assets)

        return app
