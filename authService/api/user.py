from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authService.service.user import create_user, delete_user


@api_view(['GET'])
def hello_world_test(request):
    return Response('hello world!')


@csrf_exempt
@api_view(['POST', 'DELETE'])
def basic_user_action(request):
    username = request.data.get('username')
    if request.method == 'POST':
        password = request.data.get('password')
        return create_user(username, password)
    elif request.method == 'DELETE':
        return delete_user(username)
    else:
        raise NotImplementedError
