import os

SECRET = os.getenv('SECRET')
MASTER_KEY = os.getenv('MASTER_KEY')
TOKEN_HOUR_EXPIRATION = os.getenv('TOKEN_HOUR_EXPIRATION', 6)
END_OF_PREGNANCY_IN_WEEKS = os.getenv('END_OF_PREGNANCY_IN_WEEKS', 100)