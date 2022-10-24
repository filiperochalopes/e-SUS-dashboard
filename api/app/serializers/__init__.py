from flask_marshmallow import Marshmallow
from app.models.User import User
from app.models.Medicamento import Medicamento, Receita, ViaAdministracao, FormaFarmaceutica, UnidadeMedidaTempo, TipoFrequencia
from app.models.Atendimento import Atendimento, AtendimentoProfissional, Problema
from app.models.IniciarConsulta import Cid10
from marshmallow_sqlalchemy import fields

ma = Marshmallow()

def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(ma.SQLAlchemyAutoSchema):
    """Schema that uses camel-case for its external representation
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

class AtendimentoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Atendimento


class AtendimentoProfissionalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AtendimentoProfissional
        include_relationships = True

    atendimento = fields.Nested(AtendimentoSchema)


class ProblemaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Problema
        include_relationships = True

    atendimento_profissional = fields.Nested(AtendimentoProfissionalSchema)
    cid10 = fields.Nested(Cid10Schema)

class UserSchema(CamelCaseSchema):
    class Meta:
        model = User
        include_fk = True