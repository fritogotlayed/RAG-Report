import datetime
import domain.user
import domain.metric
import domain.entity
import app.global_helpers
import collections

from app.users.decorators import requires_login
from domain.metric import Metric
from domain.entity import Entity
from flask import Blueprint, render_template, g, request
from flask.ext.sqlalchemy import SQLAlchemy
from injector import inject

__author__ = 'Frito'

mod = Blueprint('rag', __name__, url_prefix='/rag')
DATE_DISPLAY_FORMAT = '%b %d %Y'
EPOCH_TIME = datetime.datetime.utcfromtimestamp(0)


@mod.before_request
@inject(db=SQLAlchemy)
def before_request(db):
    """
    pull user's profile from the database before every request
    :param db: SQLAlchemy database
    """
    app.global_helpers.populate_user_in_session(db)


def build_selections_object(from_=None, to=None):
    now = datetime.datetime.utcnow()

    if from_ is None:
        temp = now - EPOCH_TIME - datetime.timedelta(days=7)
        from_ = int(temp.total_seconds())

    if to is None:
        temp = now - EPOCH_TIME
        to = int(temp.total_seconds())

    return {'from': from_,
            'to': to}


@mod.route('/', methods=['GET', 'POST'])
@requires_login
@inject(db=SQLAlchemy)
def home(db):
    from_ = None
    to = None

    if 'from' in request.args:
        from_ = int(request.args['from'])
    if 'to' in request.args:
        to = int(request.args['to'])

    selections = build_selections_object(from_, to)
    from_ = selections['from']
    to = selections['to']

    # Get entities that have metrics in the time frame
    query_from = datetime.datetime.utcfromtimestamp(from_)
    query_to = datetime.datetime.utcfromtimestamp(to)

    # We use the below logic instead of "between" since the between function is exclusive only.
    data = db.session.query(Entity).join(
        Entity.metrics).filter(
        Metric.date_for > query_from).filter(
        Metric.date_for <= query_to)

    # if not data:
    #     data = populate_test_data(db)

    headers = []
    display_data = []
    for entity in data:
        current_entity = {'name': entity.name, 'metrics': []}

        # For each entity we are considering, loop through the metrics and only display those that
        # are applicable to the users specified parameters.
        for metric in entity.metrics:
            if query_from.date() < metric.date_for <= query_to.date():
                if metric.date_for.strftime(DATE_DISPLAY_FORMAT) not in headers:
                    headers.append(metric.date_for.strftime(DATE_DISPLAY_FORMAT))
                current_entity['metrics'].append({'status': metric.status})

        display_data.append(current_entity)

    return render_template("rag/dashboard.html", user=g.user, entities=display_data, headers=headers,
                           selections=build_selections_object(from_, to))


def build_date_list(step=7):
    date_list = collections.OrderedDict()
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_days = 365
    days_step = step
    base = datetime.datetime.today()
    for d in [(base - datetime.timedelta(days=base.weekday() + x))
              for x in range(0, total_days, days_step)]:
        date_list[int((d - epoch).total_seconds() * 1000)] = d.strftime(DATE_DISPLAY_FORMAT)

    return date_list


# Test data generation, should be deleted once data entry is available from the UI.
def populate_test_data(db):
    data = []
    for i in range(1, 6):
        entity = Entity()
        entity.name = 'Entity %d' % (i)

        for j in range(0, 8):
            metric = Metric()
            metric.date_for = datetime.datetime.utcnow().date() - datetime.timedelta(days=j * 7)
            metric.status = 'Amber'
            entity.metrics.append(metric)

        db.session.add(entity)
        data.append(entity)

    db.session.commit()
    return data
