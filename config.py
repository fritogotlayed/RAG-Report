import os

# NOTE: It is suggested that you created a local_development.patch with git containing settings to your local
# environment. This is mainly meant to be a template for new developers to base their settings from. Also, in
# a production environment this file would be different, hopefully ;-).
__author__ = 'Frito'

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Used if an email needs to be sent to the site administrator.
ADMINS = frozenset(['youremail@yourdomain.com'])

# Define the database we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is using 2 per available processor core - to handle incoming
# requests using one and performing background operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against Cross-site Request Forgery
CSRF_ENABLED = True

# Use a secure, unique and secret key for signing the data.
CSRF_SESSOIN_KEY = 'secret csrf key'

# Secret key for signing cookies
SECRET_KEY = 'secret cookie key'

# Settings that make captcha more difficult to break :-)
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
RECAPTCHA_OPTIONS = {'theme': 'white'}
