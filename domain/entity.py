from domain import model_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Entity(model_base.Base):

    __tablename__ = 'rag_entity'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    metrics = relationship("Metric")  # Not sure if we want to keep this mapping.

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Entity %r>' % self.name