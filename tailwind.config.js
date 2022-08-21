module.exports = {
    mode: 'jit',
    content: [
        'flask_wineshop/static/node_modules/tw-elements/dist/js/**/*.js',
        'flask_wineshop/templates/*.jinja2',
        'flask_wineshop/static/src/js/*.js',
        'flask_wineshop/home/templates/*.jinja2',
        'flask_wineshop/account/templates/*.jinja2',
        'flask_wineshop/auth/templates/*.jinja2',
        'flask_wineshop/cart/templates/*.jinja2',
        'flask_wineshop/products/templates/*.jinja2',
        'flask_wineshop/blog/templates/*.jinja2',
    ],
    darkMode: false,
    theme: {
        colors: {
            'wine-red': '#972f1b',
        },
        fontFamily: {},   // TODO: load google fonts here instead of w template partial //
    },
}