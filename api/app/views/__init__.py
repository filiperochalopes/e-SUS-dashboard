from flask import Blueprint
from flask import jsonify

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

TODO Essas funções foram movidas para a API graphql e não mais terão espaço para frontend python. Estava havendo inconsistências de pacotes com python 3.11
'''

@all_views.route("/")
def hello_world():
    return jsonify({
        'msg': 'It\'s working!'
    })