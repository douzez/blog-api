from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='post@example.com', password='passtest123'):
    """ Creates a sample user """
    return get_user_model().objects.create_user(email, password)


def sample_tag(name='sample_tag'):
    """ Creates a sample tag """
    return models.Tag.objects.create(name=name)


def sample_post(title='Test Post'):
    tag1 = sample_tag(name='python')
    tag2 = sample_tag(name='tdd')
    post = models.Post.objects.create(
        user=sample_user(),
        title=title,
        body='Quisque nec erat vel eros ultricies sollicitudin sollicitudin vehicula justo. Proin egestas id dolor non pellentesque. Vivamus nec sagittis mauris. Mauris eget nunc leo. Integer ante felis, tempus nec turpis ac, interdum vehicula velit. Vestibulum ac consequat arcu. Fusce ac elit pulvinar, euismod nibh pellentesque, auctor elit.',
        description='There is no one who loves pain itself, who seeks after it and wants to have it, simply because it is pain...'
    )
    post.tags.add(tag1)
    post.tags.add(tag2)
    return post


def sample_post_published(title='TDD'):
    post = models.Post.objects.create(
        user=sample_user(),
        title=title,
        body='Quant elit pulvid nibh pellentesque, auctor elit.',
        description='There nois pain...',
        publish=True
    )
    return post


class ModelTestPost(TestCase):
    def test_create_post_with_user_successful(self):
        """ Test creates a successful post with a user """
        post = sample_post()

        self.assertEqual('Test Post', post.title)
        self.assertEqual(str(post), post.title)
        self.assertFalse(post.publish)
        tags = post.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertEqual('test-post', post.slug)

    def test_create_post_published(self):
        """ Test create a successful published post """
        post = sample_post_published()

        self.assertEqual('TDD', post.title)
        self.assertEqual('tdd', post.slug)
        self.assertTrue(post.publish)
