from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_assets import Environment

from config import config


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name=None):
    if config_name is None:
        config_name = environ.get('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # set up extensions
    assets = Environment()
    assets.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import parts of application
        from flask_wineshop.assets import compile_static_assets
        db.create_all()  # Create sql tables for our data models

        from .account import bp as account_bp
        app.register_blueprint(account_bp)

        from .auth import bp as auth_bp
        app.register_blueprint(auth_bp)

        from .api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')

        from .cart import bp as cart_bp
        app.register_blueprint(cart_bp)

        from .home import bp as home_bp
        app.register_blueprint(home_bp)

        from .products import bp as products_bp
        app.register_blueprint(products_bp)

        # Create Database Models
        db.create_all()
        compile_static_assets(assets)

        return app
