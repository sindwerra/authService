from django.test import Client, TestCase

from rest_framework.test import APIClient


class RoleTestCase(TestCase):
    def test_role_create_success(self):
        # 测试创建Role成功
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'witch'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')

    def test_create_role_fail_for_existence(self):
        # 测试创建Role成功后再次创建失败
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'warrior'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/role/add/',
            {
                'role': 'warrior'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role already exists')

    def test_delete_role_success(self):
        # 测试创建Role后删除成功
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'delete_role'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        client = APIClient()
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'delete_role'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Already Deleted.')

    def test_delete_role_failed(self):
        # 测试创建Role成功后删除失败
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'delete_role_fail'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        client = APIClient()
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'delete_role_another'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role Deletion Failed')

    def test_add_role_to_user(self):
        # 数据准备
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'add_role_suc'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/user/add/',
            {
                'username': 'bind_user_suc',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        # 测试绑定成功
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'add_role_suc',
                'user': 'bind_user_suc'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        # 测试绑定失败1：Role不存在
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'not-exist',
                'user': 'bind_user_suc'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role Does Not Exists.')
        # 测试绑定失败2：User不存在
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'add_role_suc',
                'user': 'not-exist'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'User Does Not Exists.')

    def test_check_role(self):
        # 数据准备
        # 1. 新增Role
        # 2. 新增User
        # 3. 绑定User-Role
        # 4. 获取有效Token
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'check_role_suc'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/user/add/',
            {
                'username': 'check_role_suc',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'check_role_suc',
                'user': 'check_role_suc'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'check_role_suc',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        token = r.json()
        self.assertNotEquals(token, None)

        # 测试1：Role与当前User绑定，成功
        r = client.post(
            '/api/role/check/',
            {
                'token': token,
                'role': 'check_role_suc'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), True)

        # 测试2：Token不存在，失败
        r = client.post(
            '/api/role/check/',
            {
                'token': 'not-exist',
                'role': 'check_role_suc'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Does Not Exists')

        # 测试3：Token过期，失败 TODO
        # r = client.post(
        #     '/api/role/check/',
        #     {
        #         'token': 'not-exist',
        #         'role': 'check_role_suc'
        #     }
        # )
        # self.assertEqual(r.status_code, 400)
        # self.assertEqual(r.json(), 'Token Does Not Exists')

        # 测试4：Role不存在，失败
        r = client.post(
            '/api/role/check/',
            {
                'token': token,
                'role': 'not-exist-role'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role Does Not Exists.')

        # 测试5：Role存在，但没有与User绑定，返回False
        r = client.post(
            '/api/role/add/',
            {
                'role': 'unbind_role'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/role/check/',
            {
                'token': token,
                'role': 'unbind_role'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), False)

    def test_get_roles(self):
        # 数据准备
        # 1. 新增Role a,b,c
        # 2. 新增User
        # 3. 绑定所有Role
        # 4. 获取有效Token
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/role/add/',
            {
                'role': 'b'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/role/add/',
            {
                'role': 'c'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/user/add/',
            {
                'username': 'get_roles',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'a',
                'user': 'get_roles'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'b',
                'user': 'get_roles'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'c',
                'user': 'get_roles'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'get_roles',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        token = r.json()
        self.assertNotEquals(token, None)

        # 测试1 获取当前用户的Role，成功，预期结果为3
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 3)

        # 测试2 删除一个Role再获取当前用户的Role，成功，预期结果为2
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'a',
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Already Deleted.')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

        # 测试3 使用不存在的Token获取Role，失败
        r = client.post(
            '/api/role/list/',
            {
                'token': 'does-not-exist',
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Does Not Exists')

        # 测试4 使用过期的Token获取Role，失败 TODO
        # r = client.post(
        #     '/api/role/list/',
        #     {
        #         'token': 'does-not-exist',
        #     }
        # )
        # self.assertEqual(r.status_code, 400)
        # self.assertEqual(r.json(), 'Token Does Not Exists')

        # 测试5 删除一个不存在的Role再获取当前所有Role，成功，预期结果为2
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'not-ex',
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role Deletion Failed')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

        # 测试6 删除之前已经删除的Role再获取当前所有Role，成功，预期结果为2
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'a',
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Role Deletion Failed')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

        # 测试7 删除另外一个Role，成功，预期结果为1
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'b',
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Already Deleted.')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

        # 测试8 删除另外一个Role，成功，预期结果为0
        r = client.delete(
            '/api/role/delete/',
            {
                'role': 'c',
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Already Deleted.')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)