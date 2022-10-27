from datetime import timedelta

import jwt
from django.conf import settings


def create_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'user_id': user_id,
        'access_token':'',
        'token_type':'Token'
    }