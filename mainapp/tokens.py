from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


def verify_secret_key(token):
    s = Serializer(settings.SECRET_KEY)
    try:
        token_obj = s.loads(token)
    except:
        return {}
    return token_obj


def get_secret_key(token_obj, expires_sec = 1200):
    s = Serializer(settings.SECRET_KEY, expires_sec)
    return s.dumps(token_obj).decode('utf-8')
