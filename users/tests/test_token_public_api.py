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

    def test_dont_create_token_with_invalid_credentials(self):
        """ Test that token is not created with invalid credentials """
        create_user(email='email@test.com', password='wert1234', name='Test')

        res = self.client.post(TOKEN_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
        # res.data => {'non_field_errors': [ErrorDetail(string='Unable to authenticate with provided credentials', code='authentication')]}

    def test_dont_create_token_with_no_user(self):
        """ Test that token is not created if user doesn't exist """
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # res.data => {'non_field_errors': [ErrorDetail(string='Unable to authenticate with provided credentials', code='authentication')]}

    def test_dont_create_token_with_missing_field(self):
        """ Test that token in not created with email and password are required """
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
        # res.data => {'email': [ErrorDetail(string='This field may not be blank.', code='blank')], 'password': [ErrorDetail(string='This field may not be blank.', code='blank')]}
