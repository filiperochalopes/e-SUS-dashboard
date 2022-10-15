from . import db

'''
Models relacionados aos registros de dados das gestantes
'''


class TipoGravidez(db.Model):
    __bind_key__ = "esus"

    co_tipo_gravidez = db.Column(db.Integer, primary_key=True)
    no_tipo_gravidez = db.Column(db.String)

    __tablename__ = "tb_tipo_gravidez"

    def __repr__(self):
        return '<Gravidez %r>' % self.no_tipo_gravidez


class ExamePrenatal(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_prenatal = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    qt_semana_gestacional_eco = db.Column(db.Integer)
    qt_dia_gestacional_eco = db.Column(db.Integer)
    dt_provavel_parto_eco = db.Column(db.DateTime)


class TipoEdema(db.Model):
    __bind_key__ = "esus"

    co_tipo_edema = db.Column(db.Integer, primary_key=True)
    no_tipo_edema = db.Column(db.String)

    __tablename__ = "tb_tipo_edema"

    def __repr__(self):
        return '<Edema %r>' % self.no_tipo_edema


class PreNatal(db.Model):
    __bind_key__ = "esus"

    co_seq_pre_natal = db.Column(db.Integer, primary_key=True)
    co_prontuario = db.Column(db.Integer)
    tp_gravidez = db.Column(db.Integer)
    dt_ultima_menstruacao = db.Column(db.DateTime)
    st_alto_risco = db.Column(db.Boolean)

    __tablename__ = "tb_pre_natal"

    def __repr__(self):
        return '<Pre Natal %r>' % self.co_problema


class AtendimentoProfissionalPreNatal(db.Model):
    __bind_key__ = "esus"

    # Código de atendimento profissional
    co_atend_prof_pre_natal = db.Column(db.Integer, primary_key=True)
    co_unico_pre_natal = db.Column(db.Integer)
    tp_edema = db.Column(db.Integer)  # Grau de edema
    st_gravidez_planejada = db.Column(db.Boolean)
    st_movimentacao_fetal = db.Column(db.Boolean)

    __tablename__ = "tb_atend_prof_pre_natal"

    def __repr__(self):
        return '<Atendimento Profissional de Pre Natal %r>' % self.co_atend_prof_pre_natal
