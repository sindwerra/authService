from django.urls import path

from authService.api import user, role, auth

urlpatterns = [
    path("hello-world/", user.hello_world_test),
    path("user/add/", user.add_user_action),
    path("user/delete/", user.delete_user_action),
    path("role/list/", role.get_all_roles),
    path("role/check/", role.check_role),
    path("role/assign/", role.add_role_to_user),
    path("role/add/", role.add_role_action),
    path("role/delete/", role.delete_role_action),
    path("authenticate/", auth.authenticate),
    path("invalidate/", auth.invalidate),
]
