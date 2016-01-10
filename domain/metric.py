from domain import model_base
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger, Date

__author__ = 'Frito'


class Metric(model_base.Base):

    __tablename__ = 'rag_metric'
    id = Column(Integer, primary_key=True)
    entity_for = Column(Integer, ForeignKey('rag_entity.id'), nullable=False)
    status = Column(SmallInteger, nullable=False)
    date_for = Column(Date, nullable=False)
    comments = Column(String(250))

    # TODO: Do constant lookup for status

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Metric %r>' % self.name
