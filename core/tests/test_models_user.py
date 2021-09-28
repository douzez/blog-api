from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalized_email(self):
        """ Test the email for a new user with normalized email """
        email = 'test@ExampLe.COM'
        password = 'test123pass'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())
