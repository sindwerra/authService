from django.test import Client, TestCase

from rest_framework.test import APIClient


class AuthTestCase(TestCase):
    def test_empty_username_auth(self):
        client = APIClient()
        r = client.post(
            '/api/authenticate/',
            {
                'username': '',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Username should not be empty')

    def test_empty_password_auth(self):
        client = APIClient()
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'exist',
                'password': ''
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Password should not be empty')

    def test_user_not_exist(self):
        client = APIClient()
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'exist',
                'password': '102102'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'User Does Not Exists')

    def test_user_auth_success(self):
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'auth_user',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'auth_user',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertNotEquals(r.json(), None)

    def test_user_auth_failed(self):
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'auth_user_fail',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'auth_user_fail1',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'User Does Not Exists')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'auth_user_fail',
                'password': '102102102b'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Password is not correct')

    def test_invalidate_token(self):
        # 数据准备
        # 1. 创建用户
        # 2. 获取Token
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'invalidate_user',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'invalidate_user',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        token = r.json()
        self.assertNotEquals(token, None)

        # 测试1 Token不存在
        r = client.post(
            '/api/invalidate/',
            {
                'token': 'does-not-exist'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Does Not Exists')

        # 测试2 获取用户Role列表，获取成功，结果预期为0。然后将Token失效，再次获取Role列表，失败
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)
        r = client.post(
            '/api/invalidate/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Token invalidated')
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Does Not Exists')