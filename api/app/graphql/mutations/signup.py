import os
import sys

from ariadne import convert_kwargs_to_snake_case
from app.graphql import mutation


@mutation.field('signup')
@convert_kwargs_to_snake_case
def signup(_, info, master_key: str, name: str, email: str, password: str):
    '''
    master_key: chave mestra para poder realizar temporariamente cadastro de usuários
    name: Nome do profissional a ser cadastrado
    email: Email do profissional que fara login no sistema, deve ser único
    password: Senha para acesso à plataforma
    '''

    print('Hello World', file=sys.stderr)
    print(info, file=sys.stderr)

    return {
        'name': name,
        'email': email
    }
