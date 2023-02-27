from app.models.User import User
from app.models.Medicamento import Medicamento, Receita, ViaAdministracao, FormaFarmaceutica, UnidadeMedidaTempo, TipoFrequencia
from app.models.Atendimento import Atendimento, AtendimentoProfissional, Problema, Prontuario
from app.models.IniciarConsulta import Cid10
from app.models.Cidadao import Cidadao
from app.models.Gestante import PreNatal
from app.models.Exame import ExameFisicoMedicao, ExamePrenatal, ExameRequisitado
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import fields

ma = Marshmallow()

def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

class FormaFarmaceuticaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FormaFarmaceutica


class ViaAdministracaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ViaAdministracao


class UnidadeMedidaTempoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UnidadeMedidaTempo


class TipoFrequenciaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoFrequencia


class MedicamentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Medicamento
        include_relationships = True

    forma_farmaceutica = fields.Nested(FormaFarmaceuticaSchema)


class ReceitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Receita
        include_fk = True
        load_instance = True
        include_relationships = True

    via_administracao = fields.Nested(ViaAdministracaoSchema)
    medicamento = fields.Nested(MedicamentoSchema)
    tempo_tratamento = fields.Nested(UnidadeMedidaTempoSchema)
    frequencia_dose_tempo = fields.Nested(UnidadeMedidaTempoSchema)
    tipo_frequencia_dose = fields.Nested(TipoFrequenciaSchema)


class Cid10Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cid10


class MedicaoSchema(CamelCaseSchema):
    class Meta:
        model = ExameFisicoMedicao


class ExamePrenatalSchema(CamelCaseSchema):
    class Meta:
        model = ExamePrenatal
        include_fk = True
        include_relationships = True


class ExameRequisitadoSchema(CamelCaseSchema):
    class Meta:
        model = ExameRequisitado
        include_fk = True
        load_instance = True
        include_relationships = True
    
    exames_prenatal = fields.RelatedList(fields.Nested(ExamePrenatalSchema))

        
class AtendimentoProfissionalSchema(CamelCaseSchema):
    class Meta:
        model = AtendimentoProfissional
        include_fk = True
        load_instance = True
        include_relationships = True

    medicao = fields.Nested(MedicaoSchema)
    exames_requisitados = fields.RelatedList(fields.Nested(ExameRequisitadoSchema))


class AtendimentoSchema(CamelCaseSchema):
    class Meta:
        model = Atendimento
        include_fk = True
        include_relationships = True

    atendimentos_profissionais = fields.RelatedList(fields.Nested(AtendimentoProfissionalSchema))


class ProblemaSchema(CamelCaseSchema):
    class Meta:
        model = Problema
        include_fk = True
        include_relationships = True

    atendimento_profissional = fields.Nested(AtendimentoProfissionalSchema)
    cid10 = fields.Nested(Cid10Schema)


class UserSchema(CamelCaseSchema):
    class Meta:
        model = User
        include_fk = True


class PreNatalSchema(CamelCaseSchema):
    class Meta:
        model = PreNatal
        include_relationships = True
        include_fk = True


class ProntuarioSchema(CamelCaseSchema):
    class Meta:
        model = Prontuario
        include_relationships = True
        include_fk = True

    atendimentos = fields.RelatedList(fields.Nested(AtendimentoSchema))
    prenatais = fields.RelatedList(fields.Nested(PreNatalSchema, exclude=('co_prontuario',)))


class CidadaoSchema(CamelCaseSchema):
    class Meta:
        model = Cidadao
        include_relationships = True
        include_fk = True

    prontuario = fields.Nested(ProntuarioSchema)
