from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app.users.models import User

__author__ = 'Frito'

mod = Blueprint('siteroot', __name__, url_prefix='')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/')
def home():
    return render_template("siteroot/home.html", user=g.user)
