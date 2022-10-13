import sys

from app.graphql import query
from app.utils.decorators import token_authorization


@query.field('pregnants')
@token_authorization
def pregnant(*_):

    return [
        {
            'patient': {
                'name': 'Fulana de tal',
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
