from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Post
from blog.serializers import PostSerializer

ALL_POSTS_URL = reverse('blog:all_posts')


def detail_url(post_slug):
    """ Return post detail url /api/blog/posts/:post_slug"""
    return reverse('blog:post-detail', args=[post_slug])


def create_sample_tags(number_tags=3):
    """ Creates N number of tags """
    for n in range(number_tags):
        Tag.objects.create(name='a-' + str(n))


def sample_post(user, title='Test Post', number_tags=2):
    """ Creates a sample Post """
    tags_set = Tag.objects.all()[0:number_tags]
    post = Post.objects.create(
        user=user,
        title=title,
        body='Quisque nec erat vel eros ultricies sollicitudin sollicitudin vehicula justonsequat arcu. Fusce ac elit pulvinar, euismod nibh pellentesque, auctor elit.',
        description='There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...'
    )
    for tag in tags_set:
        post.tags.add(tag)
    return post


class PublicPostsApiTests(TestCase):
    """ Tests retrieve all posts, retrieve single post with its tags """

    def setUp(self):
        create_sample_tags()
        self.user = get_user_model().objects.create_user(
            email='post@posties.com',
            password='posteandoando',
            name='The Post'
        )
        self.client = APIClient()

    def test_retrieve_all_posts(self):
        """ Test retrieving all posts """
        sample_post(self.user, 'Post 1', number_tags=3)
        sample_post(self.user, 'Post 2', number_tags=3)

        res = self.client.get(ALL_POSTS_URL, format='json')
        data = res.json()
        posts = Post.objects.all().order_by('-title')
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tags = data['results'][0]['tags']
        self.assertEqual(len(tags), 3)

    def test_retrieve_all_posts_with_pagination(self):
        """ Test retrieving all posts with pagination """
        for i in range(40):
            sample_post(self.user, 'Post' + str(i), number_tags=3)

        res = self.client.get(ALL_POSTS_URL, {'page': 4}, format='JSON')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('previous', res.data)
        self.assertIn('next', res.data)
        # ('count', 40),
        # ('next', None),
        # ('previous', 'http://testserver/api/blog/posts?page=3'),
        # ('results', [OrderedDict([('title', 'Post0'), ('get_absolute_url', '/post0')...

    def test_retrieve_one_post(self):
        """ Test retrieving one single Post """
        post = sample_post(self.user, title='One Post')

        url = detail_url(post.slug)
        res = self.client.get(url)
        serializer = PostSerializer(post)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
