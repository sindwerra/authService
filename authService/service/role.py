from rest_framework.response import Response

from authService.entity.role import role_map
from authService.entity.token import token_bucket
from authService.entity.user import user_map


def create_role(role_name):
    result = role_map.add_role(role_name)
    if result:
        return Response('Role Creation Success!')
    return Response('Role already exists', status=400)


def delete_role(role_name):
    result = role_map.remove_role(role_name)
    if result:
        return Response('Role Already Deleted.')
    # 这里只给一个general的操作失败的提示，防止出现恶意套取用户名的行为
    return Response('Role Deletion Failed', status=400)


def bind_role_to_user(role_name, user_name):
    role = role_map.get_role(role_name)
    user = user_map.get_user(user_name)
    if not role:
        return Response('Role Does Not Exists.', status=400)
    if not user:
        return Response('User Does Not Exists.', status=400)
    role.assign_user(user)
    user.bind_role(role)
    return Response('Binding Success', status=200)


def check_role_assignment(token_string, role_name):
    token = token_bucket.get_token(token_string)
    if token is None:
        return Response('Token Does Not Exists', status=400)
    if token.is_expired():
        return Response('Token Already Expired', status=400)
    role = role_map.get_role(role_name)
    if role is None:
        return Response('Role Does Not Exists.', status=400)
    user = token.user
    if role.name in user.role_binds:
        return Response(True)
    return Response(False)


def get_roles(token_string):
    token = token_bucket.get_token(token_string)
    if token is None:
        return Response('Token Does Not Exists', status=400)
    if token.is_expired():
        return Response('Token Already Expired', status=400)
    user = token.user
    return Response(user.get_roles())