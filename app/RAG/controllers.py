from datetime import datetime, timedelta
from injector import inject
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from app.RAG.models import Entity, Metric
from app.users.models import User
from app.users.decorators import requires_login

__author__ = 'Frito'

mod = Blueprint('rag', __name__, url_prefix='/rag')


@mod.before_request
@inject(db=SQLAlchemy)
def before_request(db):
    """
    pull user's profile from the database before every request
    :param db: SQLAlchemy database
    """
    g.user = None
    if 'user_id' in session:
        g.user = db.session.query(User).get(session['user_id'])


@mod.route('/', methods=['GET', 'POST'])
@requires_login
@inject(db=SQLAlchemy)
def home(db):
    data = db.session.query(Entity).all()
    if not data:
        data = populate_test_data(db)

    headers = []
    for entity in data:
        for metric in entity.metrics:
            if metric.date_for not in headers:
                headers.append(metric.date_for)
    return render_template("rag/dashboard.html", user=g.user, entities=data, headers=headers)


# Test data generation, should be deleted once data entry is available from the UI.
def populate_test_data(db):
    data = []
    for i in range(1, 6):
        entity = Entity()
        entity.name = 'Entity %d' % (i)

        for j in range(0, 8):
            metric = Metric()
            metric.date_for = datetime.utcnow().date() + timedelta(days=j*7)
            metric.status = 'Amber'
            entity.metrics.append(metric)

        db.session.add(entity)
        data.append(entity)

    db.session.commit()
    return data
