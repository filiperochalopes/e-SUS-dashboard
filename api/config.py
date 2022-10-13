import os

_basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_BINDS = {
    "local": "sqlite:///local.db"
}
JSONIFY_PRETTYPRINT_REGULAR = True
SQLALCHEMY_TRACK_MODIFICATIONS = True