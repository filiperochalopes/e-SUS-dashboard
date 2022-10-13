import sys

from functools import wraps


def token_authorization(func):
    '''Verifica se o usuário está autenticado para usar a rota'''

    @wraps(func)
    def wrapper(*args):

        print('Before code', file=sys.stderr)
        if 'Authorization' in args[1].context['request'].headers:
            token = args[1].context['request'].headers['Authorization'].split()[1]
            print(token, file=sys.stderr)

        return func(*args)

    return wrapper
