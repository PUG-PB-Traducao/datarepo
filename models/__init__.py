# this file structure follows http://flask.pocoo.org/docs/1.0/patterns/appfactories/
# initializing db in app.models.base instead of in app.__init__.py
# to prevent circular dependencies
from .base import db
from .user import UserApi
from .places import Country, PlaceType, Place
