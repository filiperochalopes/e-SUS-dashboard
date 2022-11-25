from . import db


class GrupoExame(db.Model):
    __bind_key__ = "esus"

    co_seq_tagrupoexame = db.Column(db.Integer, primary_key=True)
    co_seq_grupo_exame = db.Column(db.Integer)
    no_grupo_exame = db.Column(db.Text)
    no_sexo = db.Column(db.Text)
    nu_idade_minima = db.Column(db.Integer)
    nu_idade_maxima = db.Column(db.Integer)

    __tablename__ = "ta_grupo_exame"


class ProcedimentoGrupoExame(db.Model):
    __bind_key__ = "esus"

    co_seq_proced_grupo_exame = db.Column(db.Integer, primary_key=True)
    co_grupo_exame = db.Column(db.Integer)
    co_proced = db.Column(db.Integer)

    __tablename__ = "ta_proced_grupo_exame"


class Procedimento(db.Model):
    __bind_key__ = "esus"
    
    co_seq_proced = db.Column(db.Integer, primary_key=True)
    no_proced = db.Column(db.String)
    st_exame = db.Column(db.Integer)
    st_ativo = db.Column(db.Integer)
    tp_proced = db.Column(db.String)

    __tablename__ = "tb_proced"

    def __repr__(self):
        return f'<Procedimento {self.co_proced} - {self.no_proced}>'