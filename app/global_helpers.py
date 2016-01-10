import domain.user
import flask
import flask.ext.sqlalchemy
import injector

from flask.ext.sqlalchemy import SQLAlchemy


@injector.inject(db=SQLAlchemy)
def populate_user_in_session(db):
    """
    pull user's profile from the database before every request
    :param db: SQLAlchemy database
    """
    flask.g.user = None
    if 'user_id' in flask.session:
        flask.g.user = domain.user.get_user_by_id(db.session, flask.session['user_id'])
