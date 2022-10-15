from ariadne import gql, QueryType, MutationType

# Define type definitions (schema) using SDL
type_defs = gql(
    '''
    type Query {
        """
        Resolver para servir de fixture para models de outra aplicação Django.  
        Atenção, o campo `fields` está como **String**  
        """
        fixtures(
            "string que deve aparecer no campo model da Fixture Django"
            model:String!             
            "Opções de tabelas a serem buscadas, no momento deve ser um dos: `[ciap, cid10 , procedimento, vias, exame, medicamento, forma_farmaceutica, via_administracao]"
            table:String!): [Fixture!]

        """
        Lista de prescrições já realizadas em todo o banco de dados, útil para alimentar inteligência articifial
        """
        prescriptions: [String]
        records(cns:String): [MedicalRecord]
        recordBrief(cns:String): [MedicalRecordBrief]
        pregnants: [PregnantMedicalRecords]
    }

    type Mutation {
        signup(
            "Senha mestra para cadastro de usuários via api, já que esse recurso só consegue ser utilizado por esse meio"
            masterKey: String!, 
            """Algumas das funções disponíveis no sistema: 
            - `adm` para funções administrativas, apenas leituras, 
            - `all` para todas as funcionalidades, root, 
            - `doc` para médicos, 
            - `enf` para enfermagem e 
            - `tec` para tecnicos de enfermagem
            """
            scope: String!
            "Nome do usuário a ser criado"
            name: String!, 
            "Email do usuário criado"
            email: String!, 
            "Senha temporária do usuário"
            password: String!): User
        updatePassword(email: String!, newPassword: String!): Boolean!
        signin(username: String!, password: String!): Boolean!
        logout: Boolean!
    }

    type User{
        "Nome do usuário que será habilitado para realizar buscas nos resolvers autenticados"
        name:String!
        "Email do usuário que será habilitando para realizar buscas nos resolvers autenticados"
        email: String!
    }

    type Fixture {
        pk: String
        model: String
        fields: String
    }

    type MedicalRecord {
        patient: Patient
        problems: [String]
    }

    type PregnantMedicalRecords {
        patient: Patient
        "Data da última menstruação (LMP)"
        lastMenstrualPeriod: String
        "Idade Gestacional pela LMP"
        gestationalAgeDUM: String
        "Idade Gestacional pela USG"
        gestationalAgeUSG: String
        "**Dado importante para previse Brasil**: Número de consultas pré natais realizadas"
        prenatalVisits: Int
        "**Dado importante para previse Brasil**: Idade gestacional quando realizada a primeira consulta (Semana"
        gestationalAgeWeekFirstVisit: Int
        "**Dado importante para previse Brasil**: Idade gestacional quando realizada a primeira consulta (Semana"
        gestationalAgeDayFirstVisit: Int
        "Data prevista de parto calculada de acordo com a mais provável entre a DUM e USG"
        probableDeliveryDate: String!
        "Exames realizados no primeiro trimestre"
        firstTrimesterExams: [Exam]
        "Exames realizados no segundo trimestre"
        secondTrimesterExams: [Exam]
        "Exames realizados no terceiro trimestre"
        thirdTrimesterExams: [Exam]
        "**Dado importante para previse Brasil**: Realização de sorologia para sífilis"
        SyphilisTest: Boolean!
        "**Dado importante para previse Brasil**: Realização de sorologia para HIV"
        HIVTest: Boolean!
        "**Dado importante para previse Brasil**: Número de consultas com dentista"
        dentistVisits: Int!
        "Lista de problemas durante a gestação"
        problems: [String]
    }

    type Exam{
        "O exame foi solicitado"
        requested: Boolean!
        "O exame foi executado"
        done: Boolean!
        "Data em que o exame foi realizado"
        date: String
        "Resultado do exame"
        result: String
    }

    type ObstetricUSG{
        "Data em que foi realizada a Ultrassonografia"
        date: String
        "Idade Gestacional (Semanas) estimada no exame"
        gestationalAgeWeek: Int
        "Idade Gestacional (Dias) estimada no exame"
        gestationalAgeDay: Int
    }

    type MedicalRecordBrief {
        "Data e horário da consulta"
        datetime: String
        "Dados do paciente"
        patient: Patient
        "Assuntos dos quais se trataram a consulta"
        problems: [String]
        "Foram solicitados exames nessa consulta"
        exams: Boolean
    }

    type Patient {
        "Nome do paciente"
        name: String
        "Número do Cartão Nacional de Saúde"
        cns: String
        "Telefone de contato"
        phone: String
    }
   '''
)

# Initialize Query
query = QueryType()
# Initialize Mutation
mutation = MutationType()

import app.graphql.resolvers
