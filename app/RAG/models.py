from app import model_base
from sqlalchemy import Column, Integer, String, ForeignKey, SmallInteger, Date
from sqlalchemy.orm import relationship

__author__ = 'Frito'


class Entity(model_base.Base):

    __tablename__ = 'rag_entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    metrics = relationship("Metric")  # Not sure if we want to keep this mapping.

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Entity %r>' % self.name


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
