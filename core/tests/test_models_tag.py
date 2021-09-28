from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='tag@tags.com', password='testpassword123'):
    """ Creates a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTestTag(TestCase):
    def test_create_tag_successful(self):
        """ Test creates a successful tag """
        tag = models.Tag.objects.create(name='python')
        self.assertEqual('python', tag.name)

    def test_create_tag_str(self):
        """ Test the Tag string representation """
        tag = models.Tag.objects.create(name='vue')
        self.assertEqual(str(tag), tag.name)

    def test_create_tag_with_user(self):
        """ Test creates with an user """
        tag = models.Tag.objects.create(name='javascript', user=sample_user())
        self.assertEqual(str(tag), tag.name)
