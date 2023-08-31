from rest_framework.response import Response

from authService.entity.token import token_bucket
from authService.entity.user import user_map


def authenticate_user(username, password):
    user = user_map.get_user(username)
    if not user:
        return Response('User Does Not Exists', status=400)
    if not user.check_password(password):
        return Response('Password is not correct', status=400)
    token = token_bucket.generate_token(username, password)
    user.set_token(token)
    return Response(token.content)


def invalidate_token(token_string):
    token = token_bucket.get_token(token_string)
    if token is None:
        return Response('Token Does Not Exists', status=400)
    token_bucket.remove_token(token)
    return Response('Token invalidated')
