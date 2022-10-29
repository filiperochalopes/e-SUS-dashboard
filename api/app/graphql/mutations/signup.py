import bcrypt
import sys

from ariadne import convert_kwargs_to_snake_case
from app.models import db
from app.serializers import UserSchema
from app.env import MASTER_KEY
from app.graphql import mutation
from app.models.User import User


@mutation.field('signup')
@convert_kwargs_to_snake_case
def signup(_, info, master_key: str, scope: str, name: str, email: str, password: str):
    '''
    master_key: chave mestra para poder realizar temporariamente cadastro de usuários
    name: Nome do profissional a ser cadastrado
    email: Email do profissional que fara login no sistema, deve ser único
    password: Senha para acesso à plataforma
    '''

    if master_key == MASTER_KEY:
        # Cria um usuário em model
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(name=name, scope=scope, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        print(info, file=sys.stderr)
    else:
        raise Exception(
            'Você não tem permissões para entrar nessa rota, entre com uma masterKey correta')

    schema = UserSchema()
    return schema.dump(user)
