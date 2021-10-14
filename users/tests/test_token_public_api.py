from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicTokenApiTests(TestCase):
    """ Tests the token API """

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test.user@example.com',
            'password': 'Testpass123',
            'name': 'Test User'
        }

    def test_create_token_for_user(self):
        """ Test that a token is created for the user """
        create_user(**self.payload)

        res = self.client.post(TOKEN_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
        # rest.data = {'token': 'c09cfdf54096c3d5a8e8bb25415ccddaf0051f30'}
