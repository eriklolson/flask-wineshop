"""Routes for user authentication."""
from flask import redirect, render_template, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from flask_wineshop import login_manager
from flask_wineshop.models import User, Cart
from flask_wineshop.extensions import db

from .forms import SignupForm, LoginForm
from flask_wineshop.auth import bp

@login_manager.user_loader
def user_loader(id):
    """Check if user is logged-in on every page load."""
    if id is not None:
        return User.query.get(int(id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in for that.', 'error')
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET: Serve Log-in page.
    POST: Validate form and redirect user to index.
    """
    form = LoginForm()
    quantity_total = Cart.get_quantity_total(current_user)
    if current_user.is_authenticated:
        flash('You are already logged in', 'error')
        return redirect(url_for('home.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user)
        flash('Welcome back! You have logged in', 'success')
        return redirect(url_for('home.index'))
    else:
        return render_template('login.jinja2', form=form, quantity_total=quantity_total)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Register form to create new user accounts.
    GET: Serve register page.
    POST: Validate form, create account, redirect user to index.
    """
    form = SignupForm()
    quantity_total = Cart.get_quantity_total(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = User(
                username=form.username.data, email=form.email.data
            )
            new_user.set_password(form.password.data)
            User.save_user_to_db(new_user)
            login_user(new_user)
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('home.index', username=current_user.username))
        flash('A user already exists with that email address', 'warning')
    return render_template('signup.jinja2', form=form, quantity_total=quantity_total)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out', 'notice')
    return redirect(url_for('home.index'))



#
#
# @bp.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash(
#             _('Check your email for the instructions to reset your password'))
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password_request.html',
#                            title=_('Reset Password'), form=form)
#
#
# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash(_('Your password has been reset.'))
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
#
#
