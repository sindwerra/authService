from django.test import Client, TestCase, override_settings

from rest_framework.test import APIClient


class TokenTestCase(TestCase):

    @override_settings(TOKEN_EXPIRATION_DURATION_HOUR=0)
    def test_token_expire(self):
        # 数据准备
        # 1. 新增Role
        # 2. 新增User
        # 3. 绑定User-Role
        # 4. 获取有效Token
        client = APIClient()
        r = client.post(
            '/api/role/add/',
            {
                'role': 'expire'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Role Creation Success!')
        r = client.post(
            '/api/user/add/',
            {
                'username': 'expire',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/role/assign/',
            {
                'role': 'expire',
                'user': 'expire'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'Binding Success')
        r = client.post(
            '/api/authenticate/',
            {
                'username': 'expire',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        token = r.json()
        self.assertNotEquals(token, None)
        # 测试1 检查当前Role是否与当前User绑定，因为全局设置里Token立即过期，所以预期失败
        r = client.post(
            '/api/role/check/',
            {
                'token': token,
                'role': 'expire'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Already Expired')
        # 测试2 获取当前User的Role列表，因为全局设置里Token立即过期，所以预期失败
        r = client.post(
            '/api/role/list/',
            {
                'token': token,
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Token Already Expired')
