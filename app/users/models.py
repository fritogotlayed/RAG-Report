# from app import db
from app import model_base
from sqlalchemy import Column, Integer, String, SmallInteger
from app.users import constants as USER
__author__ = 'Frito'


class User(model_base.Base):

    __tablename__ = 'users_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    role = Column(SmallInteger, default=USER.USER)
    status = Column(SmallInteger, default=USER.NEW)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def get_status(self):
        return USER.STATUS[self.status]

    def get_role(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % self.name
