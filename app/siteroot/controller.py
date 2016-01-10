from domain.user import User
from flask import Blueprint, render_template, g, session
from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject

__author__ = 'Frito'

mod = Blueprint('siteroot', __name__, url_prefix='')


@mod.before_request
@inject(db=SQLAlchemy)
def before_request(db):
    """
    pull user's profile from the database before every request
    """
    g.user = None
    if 'user_id' in session:
        g.user = db.session.query(User).get(session['user_id'])


@mod.route('/')
def home():
    return render_template("siteroot/home.html", user=g.user)
