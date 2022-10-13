import json
from app.graphql import query

from app.models.IniciarConsulta import Ciap, Cid10, Procedimento
from app.models.Medicamento import FormaFarmaceutica, Medicamento, MedicamentoPrincipioAtivo, Receita, TipoFrequencia, TipoReceita, ViaAdministracao


@query.field("fixtures")
def fixtures(*_, table=None, model=None):
    if table == 'ciap':
        ciap_list_all = Ciap.query.all()
        return [{'model': model, 'pk': ciap.co_ciap, 'fields': json.dumps({'code': ciap.co_ciap, 'name': ciap.ds_ciap })} for ciap in ciap_list_all]
    elif table == 'cid10':
        cid10_list_all = Cid10.query.all()
        return [{'model': model, 'pk': cid10.co_cid10, 'fields': json.dumps({'code': cid10.nu_cid10, 'name': cid10.no_cid10 })} for cid10 in cid10_list_all]
    elif table == 'procedimento':
        procedimento_list_all = Procedimento.query.filter(
            Procedimento.tp_proced == 'CLINICO').filter(Procedimento.st_ativo == 1).all()
        return [{'model': model, 'pk': proced.co_proced, 'fields': json.dumps({'code': proced.co_proced, 'name': proced.no_proced })} for proced in procedimento_list_all]
    elif table == 'vias':
        vias_list_all = ViaAdministracao.query.all()
        return [{'model': model, 'pk': via_administracao.co_aplicacao_medicamento, 'fields': json.dumps({'code': via_administracao.co_aplicacao_medicamento, 'name': via_administracao.no_aplicacao_med_filtro, 'note': None })} for via_administracao in vias_list_all]
    elif table == 'exame':
        exame_list_all = Procedimento.query.filter(Procedimento.tp_proced == 'CLINICO').filter(
            Procedimento.st_ativo == 1).filter(Procedimento.st_exame == 1).all()
        return [{'model': model, 'pk': exame.co_proced, 'fields': json.dumps({'code': exame.co_proced, 'name': exame.no_proced, 'note': None })} for exame in exame_list_all]
    elif table == 'medicamento':
        medicamento_list_all = MedicamentoPrincipioAtivo.query.all()
        return [{'model': model, 'pk': m.medicamento.co_seq_medicamento, 'fields': json.dumps({'active_principle': m.medicamento.no_principio_ativo, 'concentration': m.medicamento.ds_concentracao, 'pharmaceutical_form_id': m.medicamento.co_forma_farmaceutica, 'supply_unit_id': m.medicamento.ds_unidade_fornecimento, 'recipe_type_id': m.principio_ativo.lista_medicamento.tipo_receita.co_tipo_receita })} for m in medicamento_list_all]
    elif table == 'forma_farmaceutica':
        forma_farmaceutica_list_all = FormaFarmaceutica.query.all()
        return [{'model': model, 'pk': f.co_forma_farmaceutica, 'fields': json.dumps({'code': f.co_forma_farmaceutica, 'name': f.no_forma_farmaceutica })} for f in forma_farmaceutica_list_all]
    elif table == 'via_administracao':
        via_administracao_list_all = ViaAdministracao.query.all()
        return [{'model': model, 'pk': via.co_aplicacao_medicamento, 'fields': json.dumps({'code': via.co_aplicacao_medicamento, 'name': via.no_aplicacao_med_filtro })} for via in via_administracao_list_all]
    elif table == 'tipo_receita':
        tipo_receita_list_all = TipoReceita.query.all()
        return [{'model': model, 'pk': tp_receita.co_tipo_receita, 'fields': json.dumps({'code': tp_receita.co_tipo_receita, 'name': tp_receita.no_tipo_receita })} for tp_receita in tipo_receita_list_all]
    return []