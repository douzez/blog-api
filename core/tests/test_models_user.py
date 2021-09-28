from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTestUser(TestCase):
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

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')


class ModelTestSuperUser(TestCase):
    def test_create_new_superuser(self):
        """ Test creating new super user """
        user = get_user_model().objects.create_superuser(
            'super@user.com', 'superpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_invalid_email_no_create_superuser(self):
        """ Test does not create superuser with invalid email """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(None, 'qwertyu')
