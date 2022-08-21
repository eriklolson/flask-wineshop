
from sqlalchemy import desc
from flask_wineshop.models import *
from flask_login import current_user


def get_favorites():
    favorites = db.session(Bottles).order_by(desc(Bottles.description)).all()
