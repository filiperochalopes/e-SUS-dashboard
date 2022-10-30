from . import db
from sqlalchemy.orm import relationship
import app.models.Exame
import app.models.Cidadao
import app.models.Gestante

# TODO tb_evolucao_objetivo
# TODO tb_evolucao_subjetivo
# TODO tb_evolucao_avaliacao
# TODO tb_evolucao_plano
# TODO tb_exame_requisitado


class AtendimentoProfissional(db.Model):
    '''
    Atendimento profissional é o atendimento feito por um único profissional em um dia de dida à unidade de saúde
    '''
    __bind_key__ = "esus"

    co_seq_atend_prof = db.Column(db.Integer, primary_key=True)
    dt_fim = db.Column(db.DateTime)
    dt_inicio = db.Column(db.DateTime)
    co_atend = db.Column(db.Integer, db.ForeignKey(
        'tb_atend.co_seq_atend'), nullable=True)
    
    atendimento = relationship(
        'Atendimento', uselist=False, lazy='selectin', foreign_keys=[co_atend], back_populates='atendimentos_profissionais')
    
    medicao = relationship('ExameFisicoMedicao', uselist=False, back_populates='atendimento_profissional')

    __tablename__ = "tb_atend_prof"


class Atendimento(db.Model):
    '''
    Um atendimento é como uma ida ao posto de saúde, nessa ida podem ser realizadas vários atendimentos profissionais: triagem, vacina...
    '''
    __bind_key__ = "esus"

    co_seq_atend = db.Column(db.Integer, primary_key=True)
    co_prontuario = db.Column(db.Integer, db.ForeignKey('tb_prontuario.co_seq_prontuario'))
    st_registro_tardio = db.Column(db.Integer)
    tp_local_atend = db.Column(db.Integer)

    prontuario = relationship('Prontuario', uselist=True, lazy='selectin', foreign_keys=[co_prontuario], back_populates='atendimentos')

    atendimentos_profissionais = relationship(
        'AtendimentoProfissional', uselist=True, lazy='selectin', back_populates='atendimento')

    __tablename__ = "tb_atend"


class Prontuario(db.Model):
    '''
    Cada prnotuário pertence a um indivíduo
    '''
    __bind_key__ = "esus"

    co_seq_prontuario = db.Column(db.Integer, primary_key=True)
    co_cidadao = db.Column(db.Integer, db.ForeignKey('tb_cidadao.co_seq_cidadao'))

    atendimentos = relationship('Atendimento', uselist=True, lazy='selectin', back_populates='prontuario')

    prenatais = relationship('PreNatal', uselist=True, lazy='selectin', back_populates='prontuario')

    cidadao = relationship(
        'Cidadao', uselist=False, lazy='selectin', foreign_keys=[co_cidadao], back_populates='prontuario')

    __tablename__ = "tb_prontuario"

# ? tb_problema_evolucao
# ? tb_problema
class Problema(db.Model):
    __bind_key__ = "esus"
    
    co_seq_evolucao_aval_ciap_cid = db.Column(db.Integer, primary_key=True)
    co_cid10 = db.Column(db.Integer, db.ForeignKey(
        'tb_cid10.co_cid10'), nullable=True)
    ds_nota = db.Column(db.Text)
    co_atend_prof = db.Column(db.Integer, db.ForeignKey(
        'tb_atend_prof.co_seq_atend_prof'), nullable=True)

    atendimento_profissional = relationship(
        'AtendimentoProfissional', uselist=False, lazy='selectin', foreign_keys=[co_atend_prof])
    
    cid10 = relationship(
        'Cid10', uselist=False, lazy='selectin', foreign_keys=[co_cid10])

    __tablename__ = "tl_evolucao_avaliacao_ciap_cid"

    def __repr__(self):
        return f'<Problema {self.co_cid10}>'
