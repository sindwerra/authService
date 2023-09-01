import hashlib
from dataclasses import dataclass
from typing import Set, Dict

from authService.entity.role import Role
from authService.entity.token import Token, token_bucket


class UserMap:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self._username_map = {}

    def add_user(self, username, password):
        if username in self._username_map:
            return False
        obj = User(username=username, role_binds={})
        obj.set_password(password)
        self._username_map[username] = obj
        return True

    def get_user(self, username):
        if username not in self._username_map:
            return None
        return self._username_map[username]

    def remove_user(self, username):
        if username not in self._username_map:
            return False
        user = self._username_map.pop(username)
        for _, related_role in user.role_binds.items():
            related_role.unassign_user(user)
        if hasattr(user, 'token'):
            token_bucket.remove_token(user.token)
        return True


@dataclass
class User:
    # password和token属于安全信息，不在public数据中包含
    username: str
    role_binds: Dict

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, password):
        input_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if self.password != input_password:
            return False
        return True

    def bind_role(self, role: Role):
        self.role_binds[role.name] = role

    def set_token(self, token: Token):
        self.token = token
        token.user = self

    def unbind_role(self, role):
        self.role_binds.pop(role.name, None)

    def get_roles(self):
        return self.role_binds.keys()


user_map = UserMap()
