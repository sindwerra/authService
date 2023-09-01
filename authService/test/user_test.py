from django.test import Client, TestCase

from rest_framework.test import APIClient


class UserTestCase(TestCase):

    def test_create_user_success(self):
        # 创建用户并成功
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'create_success',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')

    def test_create_user_fail_for_existence(self):
        # 创建用户并成功，然后再次创建同用户名用户失败
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'create_failed',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.post(
            '/api/user/add/',
            {
                'username': 'create_failed',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'User already exists')

    def test_user_delete_and_fail(self):
        # 删除不存在用户失败
        client = APIClient()
        r = client.delete(
            '/api/user/delete/',
            {'username': 'delete_fail'}
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'User Deletion Failed')

    def test_user_delete_and_success(self):
        # 创建用户成功，然后删除用户成功
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'delete_success',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Creation Success!')
        r = client.delete(
            '/api/user/delete/',
            {'username': 'delete_success'}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'User Already Deleted.')

    def test_empty_username_create(self):
        # 使用空用户名创建用户失败
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': '',
                'password': '102102102a'
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Username could not be empty!')

    def test_empty_password_create(self):
        # 使用空密码创建用户失败
        client = APIClient()
        r = client.post(
            '/api/user/add/',
            {
                'username': 'sindwerra',
                'password': ''
            }
        )
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), 'Password could not be empty!')
