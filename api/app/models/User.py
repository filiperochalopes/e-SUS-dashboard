from . import db
from sqlalchemy.sql import func


class User(db.Model):
    __bind_key__ = "local"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    scope = db.Column(db.String, comment='grau de permissao de acesso do usuario')
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    __tablename__ = "local_users"
