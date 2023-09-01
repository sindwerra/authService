from datetime import timedelta

from django.utils.datetime_safe import datetime

from django.conf import settings

import jwt


class TokenBucket:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self._token_map = {}

    def generate_token(self, username, password):
        token_obj = Token(username, password)
        self._token_map[token_obj.content] = token_obj
        return token_obj

    def remove_token(self, token):
        self._token_map.pop(token.content)

    def get_token(self, token_string):
        if token_string not in self._token_map:
            return None
        return self._token_map[token_string]


class Token:

    def __init__(self, username, password):
        self.expiration = datetime.now() + timedelta(hours=settings.TOKEN_EXPIRATION_DURATION_HOUR)
        self.content = jwt.encode(
            {
                "username": username,
                "exp": self.expiration,
            },
            settings.SECRET_SALT,
            algorithm='HS256'
        )
        self.user = None

    def is_expired(self):
        return True if self.expiration < datetime.now() else False

    def get_owned_user(self):
        return self.user


token_bucket = TokenBucket()
