from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag


CREATE_TAG_URL = reverse('blog:create-tag')


def detail_url(tag_slug):
    """ Return tag detail url /api/blog/tags/:tag_slug """
    return reverse('blog:update-tag', args=[tag_slug])


class PrivateTagsApiTests(TestCase):
    """ Test Tags private API create, update, delete """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='passqwert123',
            name='Taggy'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_tag_with_authetnicated_user(self):
        """ Test creating a Tag with authenticated user """
        payload = {'name': 'devops'}
        res = self.client.post(CREATE_TAG_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_tag_with_authenticated_user(self):
        """ Test updating a tag with authenticated user """
        tag = Tag.objects.create(name='avs', user=self.user)
        payload = {'name': 'aws'}

        url = detail_url(tag.slug)
        res = self.client.patch(url, payload)
        tag.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload['name'])
