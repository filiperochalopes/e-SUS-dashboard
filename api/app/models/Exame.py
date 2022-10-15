from . import db

'''
Exames de valores unitários e seriáveis
'''


class RequisicaoExame(db.Model):
    __bind_key__ = "esus"

    co_seq_requisicao_exame = db.Column(db.Integer, primary_key=True)
    dt_requisicao = db.Column(db.DateTime)
    ds_justificativa_procedimento = db.Column(db.Text)
    co_atend_prof = db.Column(db.Integer)
    co_cid10 = db.Column(db.Integer)
    ds_observacao = db.Column(db.Text)

    __tablename__ = "tb_requisicao_exame"


class TipoGlicemia(db.Model):
    __bind_key__ = "esus"

    co_tipo_glicemia = db.Column(db.Integer, primary_key=True)
    no_tipo_glicemia = db.Column(db.String)

    __tablename__ = "tb_tipo_glicemia"


class ExameFisicoMedicao(db.Model):
    __bind_key__ = "esus"

    co_seq_medicao = db.Column(db.Integer, primary_key=True)
    dt_medicao = db.Column(db.DateTime)
    co_atend_prof = db.Column(db.Integer)
    dt_ultima_menstruacao = db.Column(db.DateTime)
    nu_medicao_peso = db.Column(db.Float)
    nu_medicao_altura = db.Column(db.Float)
    nu_medicao_frequencia_cardiaca = db.Column(db.Integer)
    nu_medicao_pressao_arterial = db.Column(db.Integer)
    nu_medicao_perimetro_cefalico = db.Column(db.Integer)
    nu_medicao_frequnca_resprtria = db.Column(db.Integer)
    nu_medicao_saturacao_o2 = db.Column(db.Integer)
    tp_glicemia = db.Column(db.Integer)
    nu_medicao_glicemia = db.Column(db.Integer)
    nu_medicao_imc = db.Column(db.Float)
    nu_medicao_altura_uterina = db.Column(db.Integer)
    nu_medicao_batimnto_cardco_ftl = db.Column(db.Integer)
    nu_medicao_vacinacao_em_dia = db.Column(db.Boolean)
    nu_medicao_perimetro_panturrilha = db.Column(db.Boolean)
    nu_medicao_circunf_abdominal = db.Column(db.Boolean)

    __tablename__ = "tb_medicao"


class ExameRequisitado(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_requisitado = db.Column(db.Integer, primary_key=True)
    st_conferido = db.Column(db.Boolean)
    dt_resultado = db.Column(db.DateTime)
    co_atend_prof = db.Column(db.Integer)
    co_procecd = db.Column(db.Integer)  # Nome do exame solicitado
    co_requisicao_exame = db.Column(db.Integer)
    dt_realizacao = db.Column(db.DateTime)
    ds_resultado = db.Column(db.Text)

    __tablename__ = "tb_exame_requisitado"

    def __repr__(self):
        return '<Exame Requisitado %r>' % self.co_procecd


class ExameColesterolHDL(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_colesterol_hdl = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_colesterol_hdl = db.Column(db.Integer)

    __tablename__ = "tb_exame_colesterol_hdl"

    def __repr__(self):
        return '<Exame Colesterol HDL %r>' % self.vl_colesterol_hdl


class ExameColesterolLDL(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_colesterol_ldl = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_colesterol_ldl = db.Column(db.Integer)

    __tablename__ = "tb_exame_colesterol_ldl"

    def __repr__(self):
        return '<Exame Colesterol LDL %r>' % self.vl_colesterol_ldl


class ExameColesterolTotal(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_colesterol_total = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_colesterol_total = db.Column(db.Integer)

    __tablename__ = "tb_exame_colesterol_total"

    def __repr__(self):
        return '<Exame Colesterol Total %r>' % self.vl_colesterol_total


class ExameTriglicerideos(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_triglicerideos = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_triglicerideos = db.Column(db.Integer)

    __tablename__ = "tb_exame_triglicerideos"

    def __repr__(self):
        return '<Exame Triglicerideos %r>' % self.vl_triglicerideos


class ExameCreatitinaSerica(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_creatinina_serica = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_creatinina_serica = db.Column(db.Float)

    __tablename__ = "tb_exame_creatinina_serica"

    def __repr__(self):
        return '<Exame Creatinina Serica %r>' % self.vl_creatinina_serica


class ExameHemoglobinaGlicada(db.Model):
    __bind_key__ = "esus"

    co_seq_exame_hemoglobina_glicd = db.Column(db.Integer, primary_key=True)
    co_exame_requisitado = db.Column(db.Integer)
    vl_hemoglobina_glicada = db.Column(db.Float)

    __tablename__ = "tb_exame_hemoglobina_glicada"

    def __repr__(self):
        return '<Exame Hemoglobina Glicada %r>' % self.vl_hemoglobina_glicada
