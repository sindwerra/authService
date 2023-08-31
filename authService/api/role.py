from rest_framework.decorators import api_view
from rest_framework.response import Response

from authService.service.role import create_role, delete_role, bind_role_to_user, check_role_assignment, get_roles


@api_view(['POST', 'DELETE'])
def basic_role_action(request):
    role_name = request.data.get('role_name')
    if request.method == 'POST':
        return create_role(role_name)
    elif request.method == 'DELETE':
        return delete_role(role_name)
    else:
        raise NotImplementedError


@api_view(['POST'])
def add_role_to_user(request):
    role_name = request.data.get('role')
    user_name = request.data.get('user')
    return bind_role_to_user(role_name, user_name)


@api_view(['POST'])
def check_role(request):
    token_string = request.data.get('token')
    role_name = request.data.get('role')
    return check_role_assignment(token_string, role_name)


@api_view(['POST'])
def get_all_roles(request):
    token_string = request.data.get('token')
    return get_roles(token_string)
