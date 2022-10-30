from pprint import pp
from flask import Blueprint, render_template

import json
import pandas as pd
import plotly
import plotly.express as px

from app.models.Atendimento import Problema
from app.models.Medicamento import Medicamento, Receita
from app.serializers import ProblemaSchema

all_views = Blueprint('all', __name__,
                      template_folder='templates')

'''
- Lista de agravos mais atendidos top10
- Controle hiperdia (controles de glicemia, hba1c e pa)
- Controle gestantes
- procedimentos
- numero de atendimentos
- media atendimentos/dia
- qualidade de registro

- Colocando servidor
- Agendamentos controlados pela internet
'''


@all_views.route("/")
def dashboard():
    '''
    Tabelas envolvidas: tb_medicao
    '''
    # pacientes com diabetes
    # grafico com glicemias maiores que 200
    # grafico com pa maiores que 140/90
    # numero de pacientes com diabetes e pressao alta, asma e lista de problemas por ordem de incidencia
    cidadaos_cadastrados = None
    cidadaos_atendidos = None
    # numero de atendimentos ja registrados
    numero_atendimentos = None
    # numero de visitas domiciliares
    numero_visitas_domiciliares = None
    # numero de dias que houve atendimento
    dias_atendimento = None
    # problemas pesquisa o cidada, vê os problemas e coloca em uma lista
    pacientes_hba1c_maior_que_6 = None
    pacientes_hba1c_maior_que_7 = None
    # Prontuários está em tb_prontuario, cidadãos em tb_cidadao (nu_cns). tb_cid10 será util para descrever os problemas
    
    # This dataframe has 244 lines, but 4 distinct values for `day`
    df = px.data.tips()


    problem_schema = ProblemaSchema(many=True)
    problems = Problema.query.all()
    problems_marshmallow = problem_schema.dump(problems)
    problems_reduced = [(p['atendimento_profissional']['atendimento']['co_prontuario'], p['cid10']['nu_cid10'], f"{p['cid10']['nu_cid10']} - {p['cid10']['no_cid10_filtro']}") for p in problems_marshmallow if p['cid10'] is not None and p['atendimento_profissional']['atendimento'] is not None]
        
    df = pd.DataFrame(problems_reduced, columns=['Prontuario', 'CID10', 'Problema'])
    df = df[df['CID10'] != 'Z000']
    df = df.drop_duplicates(subset=['Prontuario', 'CID10'])
    n_df = df[['Problema']].value_counts().rename_axis('Problema').reset_index(name='Qtd')

    fig = px.pie(n_df[:20], values='Qtd', names='Problema', hole=.2)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # return render_template('index.html')
    return render_template('index.html', graphJSON=graphJSON)
