from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authService.service.user import create_user, delete_user


@api_view(['GET'])
def hello_world_test(request):
    return Response('hello world!')


@api_view(['GET'])
def index_page(request):
    return Response('This is an index page of authService, please follow the README to use it, have fun!')


@csrf_exempt
@api_view(['POST'])
def add_user_action(request):
    username = request.data.get('username')
    password = request.data.get('password')
    return create_user(username, password)


@api_view(['DELETE'])
def delete_user_action(request):
    username = request.data.get('username')
    return delete_user(username)