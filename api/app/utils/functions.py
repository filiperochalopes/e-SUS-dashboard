import sys
import jwt
import bcrypt
import datetime

from app.models.User import User
from app.env import SECRET


def generate_token(email, password) -> dict:
    '''
    Gera o token de autenticação dado o email e senha do usuário
    '''
    # Verifica se existe o email
    try:
        user = User.query.filter(email=email).one()
    except Exception as e:
        raise Exception('Não existe registro com esse email')
    
    if(bcrypt.checkpw(password, user.password)):
        encoded_jwt = jwt.encode({
        'sub': user.id,
        'scope': user.scope,
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=6)
        }, SECRET, algorithm="HS256")
    else:
        raise Exception('Senha inválida')

    print(encoded_jwt, file=sys.stderr)
    print(jwt.decode(encoded_jwt, SECRET, algorithms=["HS256"]))

    return {
        'token': encoded_jwt
    }


def check_token(token) -> dict:
    '''
    Verifica a validade do token e retorna o usuário que o está utilizando no momento
    '''
    print(jwt.decode(token, secret, algorithms=["HS256"]))
    return {}