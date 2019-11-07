from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Post

User = get_user_model()


class PostTest(TestCase):
    """ Test module for Post model """
    def setUp(self):
        author_1 = User.objects.create(username='author #1')
        author_2 = User.objects.create(username='author #2')
        Post.objects.create(title='Blog Post #1',
                            text='Dummy text #1',
                            author=author_1)
        Post.objects.create(title='Blog Post #2',
                            text='Dummy text #2',
                            author=author_2)
        Post.objects.create(title='Blog Post #3',
                            text='Dummy text #3',
                            is_published=True,
                            author=author_2)

    def test_publish_method_for_post(self):
        """ Test Post model publish method """
        post = Post.objects.get(title='Blog Post #1')
        post.publish()
        self.assertEqual(post.is_published, True)

    def test_published_post_filtering(self):
        """ Test Post Publish Object Manager for properlly filtering only
            published posts
        """
        posts = Post.published.all()
        self.assertEqual(posts.count(), 1)
