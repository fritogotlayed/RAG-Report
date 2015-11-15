from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.users.forms import RegisterForm, LoginForm
from app.users.models import User
from app.users.decorators import requires_login

__author__ = 'Frito'

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/me/')
@requires_login
def home():
    return render_template("users/profile.html", user=g.user)


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    return render_template('users/login.html', form=form)


@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # Create a user instance
        user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))

        # Store it in the db
        db.session.add(user)
        db.session.commit()

        # "log" the user in
        session['user_id'] = user.id

        flash('Thanks for registering')
        return redirect(url_for('users.home'))
    return render_template('users/register.html', form=form)


@mod.route('/logout/', methods=['GET', 'POST'])
def logout():
    """
    Logout form
    """
    session.pop('user_id', None)

    if request.referrer is None:
        return redirect(url_for('siteroot.home'))

    return redirect(request.referrer)
