from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """ Test the users public API """

    def setUp(self):
        self.payload = {
            'email': 'test.user@example.com',
            'password': 'Testpass123',
            'name': 'Test User'
        }
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test creating a user with valid payload is successful """
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)
        # res.data => {'email': 'test.user@example.com', 'name': 'Test User'}

    def test_does_not_create_user_that_exists(self):
        """ Test does not create an user that already exists """
        create_user(**self.payload)

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(res.data), 1)
        self.assertIn('email', res.data)
        # res.data => {'email': [ErrorDetail(string='user with this email already exists.', code='unique')]}

    def test_does_not_create_user_password_too_short(self):
        """ Test that password must be more >= 8 characters """
        payload = {
            'email': 'test.user@example.com',
            'password': 'qwertyu',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)
