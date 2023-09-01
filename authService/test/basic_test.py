from django.test import Client, TestCase

from rest_framework.test import APIClient


class BasicTestCase(TestCase):

    def test_hello_world(self):
        client = APIClient()
        r = client.get('/api/hello-world/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'hello world!')