from rest_framework.response import Response

from authService.entity.user import user_map


def create_user(username, password):
    result = user_map.add_user(username, password)
    if result:
        return Response('User Creation Success!')
    return Response('User already exists', status=400)


def delete_user(username):
    result = user_map.remove_user(username)
    if result:
        return Response('User Already Deleted.')
    # 这里只给一个general的操作失败的提示，防止出现恶意套取用户名的行为
    return Response('User Deletion Failed', status=400)
