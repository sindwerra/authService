from dataclasses import dataclass
from typing import Dict


class RoleMap:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self._role_map = {}

    def add_role(self, role_name):
        if role_name in self._role_map:
            return False
        obj = Role(role_name, {})
        self._role_map[role_name] = obj
        return True

    def remove_role(self, role_name):
        if role_name not in self._role_map:
            return False
        role = self._role_map.pop(role_name)
        for _, related_user in role.user_assignments.items():
            related_user.unbind_role(role.name)
        return True

    def get_role(self, role_name):
        if role_name not in self._role_map:
            return None
        return self._role_map[role_name]


@dataclass
class Role:
    name: str
    user_assignments: Dict

    def assign_user(self, user):
        self.user_assignments[user.username] = user

    def unassign_user(self, user):
        self.user_assignments.pop(user.username, None)


role_map = RoleMap()
