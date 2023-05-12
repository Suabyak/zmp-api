from rest_framework_jwt.settings import api_settings
import jwt

def get_token_for_user(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    
    return token

def get_user_from_token(token):
    if not is_token_valid(token):
        raise WrongTokenException("Token is not valid")
    payload = api_settings.JWT_DECODE_HANDLER(token)
    
    return payload

def is_token_valid(token):
    try:
        jwt.decode(token, api_settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return True
    except:
        return False

class WrongTokenException(Exception):
    pass