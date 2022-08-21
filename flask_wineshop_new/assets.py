from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Configure and build asset bundles."""
    assets.auto_build = True
    assets.debug = False

    # Global asset bundles
    common_style_bundle = Bundle(
        'src/scss/global.scss',
        filters='scss,cssmin',
        output='dist/css/global.css',
        extra={'rel': 'stylesheet/scss'},
    )
    common_js_bundle = Bundle(
        'src/js/main.js',
        filters='jsmin',
        output='dist/js/main.min.js',
        extra={'rel': 'stylesheet/scss'},
    )

    # Local asset bundles
    account_style_bundle = Bundle(
        'account/scss/account.scss',
        filters='scss,cssmin',
        output='dist/css/account.css',
        extra={'rel': 'stylesheet/scss'},
    )
    auth_style_bundle = Bundle(
        'auth/scss/*.scss',
        filters='scss,cssmin',
        output='dist/css/auth.css',
        extra={'rel': 'stylesheet/scss'},
    )
    cart_style_bundle = Bundle(
        'cart/scss/cart.scss',
        filters='scss,cssmin',
        output='dist/css/cart.css',
        extra={'rel': 'stylesheet/scss'},
    )
    home_style_bundle = Bundle(
        'home/scss/index.scss',
        filters='scss,cssmin',
        output='dist/css/index.css',
        extra={'rel': 'stylesheet/scss'},
    )
    products_style_bundle = Bundle(
        'products/scss/*.scss',
        filters='scss,cssmin',
        output='dist/css/wine.css',
        extra={'rel': 'stylesheet/scss'}
    )

    assets.register('common_style_bundle', common_style_bundle)
    assets.register('common_js_bundle', common_js_bundle)
    assets.register('account_style_bundle', account_style_bundle)
    assets.register('auth_style_bundle', auth_style_bundle)
    assets.register('cart_style_bundle', cart_style_bundle)
    assets.register('home_style_bundle', home_style_bundle)
    assets.register('products_style_bundle', products_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_style_bundle.build()
        common_js_bundle.build()
        account_style_bundle.build()
        auth_style_bundle.build()
        cart_style_bundle.build()
        home_style_bundle.build()
        products_style_bundle.build()
    return assets