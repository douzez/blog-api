from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Post
from blog.serializers import TagDetailSerializer

# CREATE_TAG_URL = reverse('blog:create')
ALL_TAGS_URL = reverse('blog:all-tags')


def detail_url(tag_slug):
    """ Return tag detail url """
    # /api/blog/tags/<slug>
    return reverse('blog:tag-detail', args=[tag_slug])


class PublicTagsApiTests(TestCase):
    """ Tests retrieve all tags, retrieve tag with its posts endpoints without authentication """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='tag@taggy.com',
            password="tageandoando",
            name="The Tag"
        )
        self.client = APIClient()

    def test_retrieve_tags(self):
        """ Test retrieving all tags """
        Tag.objects.create(user=self.user, name='python')
        Tag.objects.create(user=self.user, name='css')

        res = self.client.get(ALL_TAGS_URL)

        tags = Tag.objects.all().order_by('name')
        serializer = TagDetailSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        """
        res [OrderedDict([('id', '8be37839-4666-4517-b86f-9116c396dafe'), ('name', 'css')]), OrderedDict([('id', '1893116c-846b-4ff6-9ab0-61fd64fbfd20'), ('name', 'python')])]
        serializer [OrderedDict([('id', '8be37839-4666-4517-b86f-9116c396dafe'), ('name', 'css')]), OrderedDict([('id', '1893116c-846b-4ff6-9ab0-61fd64fbfd20'), ('name', 'python')])]
        """

    def test_retrieve_one_tag(self):
        """ Test retrieving one single tag """
        tag = Tag.objects.create(user=self.user, name='Python JS')

        url = detail_url(tag.slug)
        res = self.client.get(url)
        serializer = TagDetailSerializer(tag)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_one_tag_with_its_posts(self):
        """ Test retrieving a tag with its posts """
        tag = Tag.objects.create(user=self.user, name='postie tag')
        post = Post.objects.create(
            user=self.user,
            title='Post with tags',
            body='Quisque nec era, auctor elit.',
            description='There is...'
        )
        post2 = Post.objects.create(
            user=self.user,
            title='Post with tags 2',
            body='Quisque nec era, auctor elit.',
            description='There is...'
        )
        Post.objects.create(
            user=self.user,
            title='Post without tags',
            body='Quisque nec era, auctor elit.',
            description='There is...'
        )
        tag.posts.add(post)
        tag.posts.add(post2)
        url = detail_url(tag.slug)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['posts']), 2)
        self.assertIn('post-with-tags', res.data['posts'])
        # res.data ==> {'name': 'postie tag', 'slug': 'postie-tag', 'get_absolute_url': '/postie-tag', 'posts': ['post-with-tags-2', 'post-with-tags']}
