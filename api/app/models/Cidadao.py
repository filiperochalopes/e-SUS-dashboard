from . import db
from sqlalchemy.orm import relationship

class Cidadao(db.Model):
    __bind_key__ = "esus"
    
    co_seq_cidadao = db.Column(db.Integer, primary_key=True)
    no_cidadao = db.Column(db.Text)
    nu_cns = db.Column(db.Text)
    nu_telefone_residencial = db.Column(db.Text)
    nu_telefone_celular = db.Column(db.Text)
    nu_telefone_contato = db.Column(db.Text)
    no_sexo = db.Column(db.Text)
    dt_nascimento = db.Column(db.DateTime)

    prontuario = relationship(
        'Prontuario', uselist=False, lazy='selectin', back_populates='cidadao')

    __tablename__ = "tb_cidadao"

    def __repr__(self):
        return '<User %r>' % self.nu_cns