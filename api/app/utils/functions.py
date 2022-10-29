import jwt
import bcrypt
import datetime

from app.models import db
from app.models.User import User
from app.env import SECRET, TOKEN_HOUR_EXPIRATION

def generate_token(email, password) -> dict:
    '''
    Gera o token de autenticação dado o email e senha do usuário
    '''
    try:
        # Verifica se existe o email
        user = db.session.query(User).filter(User.email==email).one()
    except Exception as e:
        raise Exception(f'{e} Não existe usuário com esse email')

    # Cria um usuário em model
    if(bcrypt.checkpw(password.encode('utf-8'), user.password)):
        encoded_jwt = jwt.encode({
            'sub': user.id,
            'scope': user.scope,
            'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=TOKEN_HOUR_EXPIRATION)
        }, SECRET, algorithm="HS256")
    else:
        raise Exception('Senha inválida')

    return {
        'user': user,
        'token': encoded_jwt
    }


def check_token(token) -> dict:
    '''
    Verifica a validade do token e retorna o usuário que o está utilizando no momento
    '''

    decoded_jwt = jwt.decode(token, SECRET, algorithms=["HS256"])
    user = db.session.query(User).get(decoded_jwt['sub'])

    return {
        'user': user,
        'token': token
    }