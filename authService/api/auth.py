from rest_framework.decorators import api_view
from rest_framework.response import Response

from authService.service.auth import authenticate_user, invalidate_token


@api_view(['POST'])
def authenticate(request):
    username = request.data.get('username')
    password = request.data.get('password')
    return authenticate_user(username, password)


@api_view(['POST'])
def invalidate(request):
    token_string = request.data.get('token')
    return invalidate_token(token_string)
