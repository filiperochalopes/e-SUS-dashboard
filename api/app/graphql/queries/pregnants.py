from calendar import week
from pprint import pprint
import sys
from app.serializers import CidadaoSchema
from app.models.Gestante import PreNatal
from datetime import datetime, timedelta, timezone

from app.graphql import query
from app.utils.decorators import token_authorization
from app.models.User import User
from app.models import db

@query.field('pregnants')
@token_authorization
def pregnant(*_, current_user: User):
    
    # Verifica todas as consultas prenatais
    prenatal = db.session.query(PreNatal).all()
    # Avalia todos os usuários das consultas pré natais, retirando aquelas que tem mais de 42 semanas desde a data registrada de última menstruação para remover as que já tiveram os bebês
    pregnants = [p.prontuario.cidadao for p in prenatal if (datetime.now(timezone.utc) - p.dt_ultima_menstruacao).days/7 < 60]
    print('---------- Prenatais ----------', file=sys.stderr)
    schema = CidadaoSchema()
    pprint([schema.dump(p) for p in pregnants], stream=sys.stderr)
    print('---------- --------- ----------', file=sys.stderr)


    return [
        {
            'patient': {
                'name': current_user.name,
                'cns': '123456781234567',
                'phone': '75982564785'
            },
            'lastMenstrualPeriod': '2022/10/05',
            'gestationalAgeDUM': '15s6d',
            'gestationalAgeUSG': '16s0d',
            'prenatalVisits': 4,
            'gestationalAgeWeekFirstVisit': 8,
            'gestationalAgeDayFirstVisit': 2,
            'probableDeliveryDate': '2022/01/02',
            'firstTrimesterExams': [],
            'secondTrimesterExams': [],
            'thirdTrimesterExams': [],
            'SyphilisTest': True,
            'HIVTest': False,
            'dentistVisits': 0,
            'problems': []
        }
    ]
