from flask import url_for, request, render_template
from sqlalchemy import desc
from flask_login import current_user

from flask_wineshop.models import Bottles, Countries, Regions, Cart
from flask_wineshop.extensions import db
from flask import current_app as app
from flask_wineshop.products import bp


@bp.route('/product-page/<int:bottles_id>')
def product_page(bottles_id):
    quantity_total = Cart.get_quantity_total(current_user)
    product = Bottles.query.get(bottles_id)
    bottles = db.session.query(Bottles).order_by(desc(Bottles.description)).all()
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    return render_template("product-page.jinja2", product=product, bottles=bottles, countries=countries, colors=colors,
                           varietals=varietals, regions=regions,  quantity_total=quantity_total)


@bp.route('/wine')
def wine():
    page = request.args.get('page', 1, type=int)
    quantity_total = Cart.get_quantity_total(current_user)
    bottles = Bottles.query.order_by(desc(Bottles.description)).paginate(
        page=page, per_page=app.config['WINES_PER_PAGE'], error_out=False)
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    next_url = url_for('products.wine', page=bottles.next_num) if bottles.has_next else None
    prev_url = url_for('products.wine', page=bottles.prev_num) if bottles.has_prev else None
    return render_template("wine.jinja2", bottles=bottles.items, countries=countries, colors=colors,
                           varietals=varietals, regions=regions, next_url=next_url, prev_url=prev_url,
                           quantity_total=quantity_total, title='wine')


@bp.route('/color/<color_name>')
def color(color_name):
    page = request.args.get('page', 1, type=int)
    quantity_total = Cart.get_quantity_total(current_user)
    bottles = db.session.query(Bottles).filter_by(color_name=color_name).paginate(
        page=page, per_page=app.config['WINES_PER_PAGE'], error_out=False)
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    next_url = url_for('products.color', color_name=color_name, page=bottles.next_num) if bottles.has_next else None
    prev_url = url_for('products.color', color_name=color_name, page=bottles.prev_num) if bottles.has_prev else None
    return render_template('results.jinja2', bottles=bottles.items, countries=countries, colors=colors,
                           varietals=varietals, regions=regions, next_url=next_url, prev_url=prev_url,
                           quantity_total=quantity_total)


@bp.route('/varietal/<primary_grape>')
def varietal(primary_grape):
    page = request.args.get('page', 1, type=int)
    quantity_total = Cart.get_quantity_total(current_user)
    bottles = db.session.query(Bottles).filter_by(primary_grape=primary_grape).paginate(
        page=page, per_page=app.config['WINES_PER_PAGE'], error_out=False)
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    next_url = url_for('products.varietal', primary_grape=varietal, page=bottles.next_num) if bottles.has_next else None
    prev_url = url_for('products.varietal', primary_grape=varietal, page=bottles.prev_num) if bottles.has_prev else None
    return render_template('results.jinja2', bottles=bottles.items, countries=countries, colors=colors,
                           varietals=varietals, regions=regions, next_url=next_url, prev_url=prev_url,
                           quantity_total=quantity_total)


@bp.route("/country/<country_name>")
def country(country_name):
    page = request.args.get('page', 1, type=int)
    quantity_total = Cart.get_quantity_total(current_user)
    bottles = db.session.query(Bottles).filter_by(country_name=country_name).paginate(
        page=page, per_page=app.config['WINES_PER_PAGE'], error_out=False)
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    next_url = url_for('products.country', country_name=country_name, page=bottles.next_num) if bottles.has_next else None
    prev_url = url_for('products.country', country_name=country_name, page=bottles.prev_num) if bottles.has_prev else None
    return render_template('results.jinja2', bottles=bottles.items, ccountries=countries, colors=colors,
                           varietals=varietals, regions=regions, next_url=next_url, prev_url=prev_url,
                           quantity_total=quantity_total)


@bp.route("/region/<region_name>")
def region(region_name):
    page = request.args.get('page', 1, type=int)
    quantity_total = Cart.get_quantity_total(current_user)
    bottles = db.session.query(Bottles).filter_by(region_name=region_name).paginate(
        page=page, per_page=app.config['WINES_PER_PAGE'], error_out=False)
    colors = Bottles.query.with_entities(Bottles.color_name).distinct().order_by(Bottles.color_name.asc())
    varietals = Bottles.query.with_entities(Bottles.primary_grape).distinct().order_by(Bottles.primary_grape.asc())
    countries = Countries.query.with_entities(Countries.country_name).distinct().order_by(Countries.country_name.asc())
    regions = Regions.query.with_entities(Regions.region_name).distinct().order_by(Regions.region_name.asc())
    next_url = url_for('products.region', region_name=region_name, page=bottles.next_num) if bottles.has_next else None
    prev_url = url_for('products.region', region_name=region_name, page=bottles.prev_num) if bottles.has_prev else None
    return render_template('results.jinja2', bottles=bottles.items, countries=countries, colors=colors,
                           varietals=varietals, regions=regions, next_url=next_url, prev_url=prev_url,
                           quantity_total=quantity_total)
