from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


MU_URL = reverse('user:mu')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PrivateUserApiTest(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email='test@auth.com',
            password='Qwerty81672',
            name='Auth Testson'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_successful(self):
        """ Test retrieving profile logged in user """
        res = self.client.get(MU_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {'name': self.user.name, 'email': self.user.email}
        )

    def test_post_mu_not_allowed(self):
        """ Test that POST is not allowed on the mu url """
        res = self.client.post(MU_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test updating the user profile for authenticated user """
        payload = {'name': 'Updation', 'password': 'newpassword'}

        res = self.client.patch(MU_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PublicUserApiTest(TestCase):
    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        res = self.client.get(MU_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
