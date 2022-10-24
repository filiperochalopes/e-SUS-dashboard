import sys

from functools import wraps

from app.utils.functions import check_token


def token_authorization(func):
    '''Verifica se o usuário está autenticado para usar a rota'''

    @wraps(func)
    def wrapper(*args, **kwargs):

        if 'Authorization' in args[1].context['request'].headers:
            token = args[1].context['request'].headers['Authorization'].split()[1]
            # Verifica se o token é valido
            if not token:
                raise Exception('Token ausente ou inválido')
            user, token = check_token(token).values()
            print(user, file=sys.stderr)
            if not user:
                raise Exception('Token inválido')
        else:
            raise Exception('Token ausente. Adicione o Header Authorization: Bearer Token')

        return func(*args, **kwargs, current_user=user)

    return wrapper
