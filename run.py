import os
import sys

from app.model_base import Base
from flask import Flask, render_template
from flask.ext.injector import FlaskInjector
from flask.ext.sqlalchemy import SQLAlchemy
from injector import Module, singleton, Injector

__author__ = 'Frito'


def install_secret_key(application, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(application.instance_path, filename)

    try:
        application.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)


def build_app():
    CONFIG_OBJECT = os.environ.get('RAG_CONFIG', 'config')

    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(CONFIG_OBJECT)

    if not app.config['DEBUG']:
        install_secret_key(app)

    # The from/import being here is okay since we do not want __init__ in our packages executing yet.
    from app.users.controllers import mod as users_module  # noqa: skips the pep8 violation here.
    from app.siteroot.controller import mod as siteroot_module  # noqa: skips the pep8 violation here.
    from app.RAG.controllers import mod as rag_module  # noqa: skips the pep8 violation here.
    app.register_blueprint(users_module)
    app.register_blueprint(siteroot_module)
    app.register_blueprint(rag_module)

    injector = Injector([ApplicationInitializer(app)])
    FlaskInjector(app=app, injector=injector)

    return app


def main():
    app = build_app()
    app.run(host='127.0.0.1', port=8000, debug=True)


class ApplicationInitializer(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        db = self.configure_db(self.app)
        binder.bind(SQLAlchemy, to=db, scope=singleton)

    def configure_db(self, app):
        db = SQLAlchemy(app)
        Base.metadata.create_all(db.engine)
        return db


if __name__ == '__main__':
    main()
