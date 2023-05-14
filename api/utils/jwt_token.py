from rest_framework_jwt.settings import api_settings
import jwt
from .models import serialize_user
from django.contrib.auth.models import User

def get_token_for_user(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    
    return token

def get_user_from_token(token):
    token = token.split(" ")[1]
    if not is_token_valid(token):
        raise WrongTokenException("Token is not valid")
    payload = api_settings.JWT_DECODE_HANDLER(token)
    user = User.objects.filter(id=payload["user_id"]).first()
    user = serialize_user(user)
    return user

def is_token_valid(token):
    try:
        jwt.decode(token, api_settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return True
    except:
        return False

class WrongTokenException(Exception):
    pass