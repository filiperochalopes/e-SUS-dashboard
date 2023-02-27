from calendar import week
from pprint import pprint
import sys
import re
from app.serializers import CidadaoSchema
from app.models.Gestante import PreNatal
from datetime import datetime, timedelta, timezone, date

from app.graphql import query
from app.utils.decorators import token_authorization
from app.models.User import User
from app.models import db
from app.env import END_OF_PREGNANCY_IN_WEEKS

class Pregnancy:
    def __init__(self, last_menstrual_period:date, first_usg_date:date=None, first_usg_gestational_weeks:int=None, first_usg_gestational_days:int=None):
        print("Iniciando inicialização", file=sys.stderr)
        self.last_menstrual_period = last_menstrual_period.date()
        self.first_usg_gestational_weeks = first_usg_gestational_weeks
        self.first_usg_gestational_days = first_usg_gestational_days
        self.first_usg_date = first_usg_date.date() if first_usg_date else None
        self.lmp_gestational_age = self.get_gestational_age()[0]
        self.usg_gestational_age = self.get_gestational_age()[1]
        self.initial_date = self.get_initial_date()
        self.gestational_age = self.get_gestational_age()[2]
        self.due_date = self.get_gestational_due_date()
        self.first_trimester_ending_date = self.initial_date + timedelta(weeks=13, days=6)
        self.second_trimester_ending_date = self.initial_date + timedelta(weeks=27, days=6)
        self.third_trimester_ending_date = self.initial_date + timedelta(weeks=42, days=6)
        print("Finalizando inicialização", file=sys.stderr)
    
    def get_initial_date(self):
        print("Iniciando set_initial_date", file=sys.stderr)
        '''Calcula a data inicial da forma mais eficiente
        Reference: https://pubmed.ncbi.nlm.nih.gov/12501080
        https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/05/methods-for-estimating-the-due-date
        A forma mais eficiente de  verificar é pela primeira USG com menos de 13s6d, ou seja USG de primeiro trimestre. Se a diferença entre a data pela LMP for:
            Greater than 5 days before 9 0/7 weeks of gestation by LMP
            Greater than 7 days from 9 0/7 weeks to 15 6/7 weeks by LMP
            Greater than 10 days from 16 0/7 weeks to 21 6/7 weeks by LMP
            Greater than 14 days from 22 0/7 weeks to 27 6/7 weeks by LMP
            Greater than 21 days after 28 0/7 weeks by LMP
        Assumir a data da USG. Ref.: ACOG
        '''
        initial_date = date.today()
        # Verifica se existe alguma ultrassonografia, se não existir retorna a data inicial com base na dum (LMP)
        if self.first_usg_date is None:
            print('Breakpoint 1', file=sys.stderr)
            w, d = Pregnancy.split_gestational_age_string(self.lmp_gestational_age)
            return date.today() - timedelta(weeks=w, days=d)
        # Calculo a idade gestacional pela dum no período da primeira ultrassonografia
        print('Breakpoint 2', file=sys.stderr)
        lmp_gestational_age_at_first_usg_time = self.get_gestational_age(reference_date=self.first_usg_date)[0]
        # Calculo a diferenca entre os períodos
        print('Breakpoint 3', file=sys.stderr)
        lmp_w, lmp_d = Pregnancy.split_gestational_age_string(lmp_gestational_age_at_first_usg_time)
        usg_w, usg_d = (self.first_usg_gestational_weeks, self.first_usg_gestational_days)
        difference_days = abs((timedelta(weeks=lmp_w, days=lmp_d) - timedelta(weeks=usg_w, days=usg_d)).days)
        # Se corresponder a algum dos critérios usa a base
        print('Breakpoint 4', file=sys.stderr)
        if (lmp_w < 9 and difference_days > 5) or (lmp_w >= 9 and lmp_w < 16 and difference_days > 7) or (lmp_w >= 16 and lmp_w < 22 and difference_days > 10) or (lmp_w >= 22 and lmp_w < 28 and difference_days > 14) or (lmp_w >= 28 and difference_days > 21):
            initial_date = self.first_usg_date - timedelta(weeks=usg_w, days=usg_d)
        else:
            initial_date = self.first_usg_date - timedelta(weeks=lmp_w, days=lmp_d)
        print('===================================', file=sys.stderr)
        print('defining self.initial_date', file=sys.stderr)
        print(initial_date, file=sys.stderr)
        print('===================================', file=sys.stderr)
        return initial_date
        
    def get_gestational_due_date(self) -> date:
        print("Iniciando get_gestational_due_date", file=sys.stderr)
        '''Calcula a data prevista de parto assumindo um ciclo de 28 dias com ovulação ocorrendo no décimo quarto dia. Pode ocorrer então um erro de mais de 2 semanas. Em caso de sabido exatamente a data de fertilização como em vitro, adicionar 266 dias do dia da concepção
        '''
        return self.initial_date + timedelta(days=280)

    @staticmethod
    def split_gestational_age_string(string) -> tuple:
        splited = re.split(r'\D', string)
        print('splited', file=sys.stderr)
        print(splited, file=sys.stderr)
        return (int(splited[0]), int(splited[1]))

    def get_trimester(self, exam_date:date):
        '''Captura o trimestre do qual o exame faz parte
        Return -1 Em caso de o exame ter sido realizado antes da gestação atual
                1 Em caso do primeiro trimestre 1 - 13s6d semanas
                2 Em caso do segundo trimestre 14 - 27s6d semanas
                3 Em caso do terceiro trimestre 28 - 40s6d semanas
                4 Em caso de ser realizado depois dos último trimestre
        '''
        # Verifica a qual a "idade gestacional" até a data atual
        if exam_date < self.initial_date:
            return -1
        elif exam_date <= self.first_trimester_ending_date:
            return 1
        elif exam_date <= self.second_trimester_ending_date:
            return 2
        elif exam_date <= self.third_trimester_ending_date:
            return 3
        else:
            return 4

    def get_gestational_age(self, reference_date:date=date.today()) -> tuple:
        ''' Captura a idade gestacional tomando por referencia uma determinada data.

        Return tuple (str: lmp_gestational_age, str: usg_gestational_age, str: definitive_gestational_age)
        '''
        lmp_ga_string = None
        usg_ga_string = None
        def_ga_string = None
        
        def weeks_and_days_string(minus_date:date):
            total_days = (reference_date - minus_date).days
            return f'{total_days // 7}s{total_days % 7}d'

        if self.last_menstrual_period:
            lmp_ga_string = weeks_and_days_string(self.last_menstrual_period)
        if self.first_usg_date:
            w, d = Pregnancy.split_gestational_age_string(weeks_and_days_string(self.first_usg_date))
            w = self.first_usg_gestational_weeks + w
            d = self.first_usg_gestational_days + d
            usg_ga_string = f'{w}s{d}d'
        if hasattr(self, 'initial_date') and self.initial_date:
            def_ga_string = weeks_and_days_string(self.initial_date)

        return (lmp_ga_string, usg_ga_string, def_ga_string)


@query.field('pregnants')
@token_authorization
def pregnant(*_, current_user: User):
    
    # Verifica todas as consultas prenatais
    prenatal = db.session.query(PreNatal).all()
    # Avalia todos os usuários das consultas pré natais, retirando aquelas que tem mais de 42 semanas desde a data registrada de última menstruação para remover as que já tiveram os bebês
    pregnants = [p.prontuario.cidadao for p in prenatal if (datetime.now(timezone.utc) - p.dt_ultima_menstruacao).days/7 < END_OF_PREGNANCY_IN_WEEKS]
    print('---------- Prenatais ----------', file=sys.stderr)
    schema = CidadaoSchema()
    pprint([schema.dump(p) for p in pregnants], stream=sys.stderr)
    print('---------- --------- ----------', file=sys.stderr)
    pregnants = [schema.dump(p) for p in pregnants]
    
    pregnants_return = []
    if len(pregnants) > 0:
        for p in pregnants:
            # Verifica a primeira ultrassonografia
            prenatal_usg = []
            print('---------- Exames ----------', file=sys.stderr)
            for schedule in p['prontuario']['atendimentos']:
                for professional_service in schedule['atendimentosProfissionais']:
                    for exam in professional_service['examesRequisitados']:
                        for prenatal_exams in exam['examesPrenatal']:
                            print(prenatal_exams, file=sys.stderr)
            print('---------- ------ ----------', file=sys.stderr)

            # Verifica os exames de sangue
            first_trimester_exams = []
            second_trimester_exams = []
            third_trimester_exams = []

            print('Criando instância Pregnancy', file=sys.stderr)
            pregnancy = Pregnancy(
                last_menstrual_period=datetime.strptime(p['prontuario']['prenatais'][-1]['dtUltimaMenstruacao'], '%Y-%m-%dT%H:%M:%S%z')
            )

            print('Adicionando nova gestante', file=sys.stderr)
            pregnants_return.append({
            'patient': {
                    'id': p['coSeqCidadao'],
                    'name': p['noCidadao'],
                    'cns': p['nuCns'],
                    'phone': p['nuTelefoneCelular'],
                    'birthDay': p['dtNascimento'],
                },
            'lastMenstrualPeriod': pregnancy.last_menstrual_period,
            'gestationalAgeDUM': pregnancy.lmp_gestational_age,
            'gestationalAgeUSG': pregnancy.usg_gestational_age,
            'gestationalAge': pregnancy.gestational_age,
            'prenatalVisits': len(p['prontuario']['prenatais']),
            'gestationalAgeFirstVisit': pregnancy.get_gestational_age,
            'probableDeliveryDate': '2022/01/02',
            'firstTrimesterExams': [],
            'secondTrimesterExams': [],
            'thirdTrimesterExams': [],
            'SyphilisTest': True,
            'HIVTest': False,
            'dentistVisits': 0,
            'problems': []
        })
    
    print(pregnants_return, file=sys.stderr)    
    return pregnants_return
