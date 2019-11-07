import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Post
from ..serializers import BlogPostDetailSerializer, BlogPostListSerializer

User = get_user_model()
# initialize the APIClient app
client = Client()


class GetAllPostsTest(TestCase):
    """ Test module for GET all posts API """
    def setUp(self):
        author = User.objects.create(username='author #1')
        Post.objects.create(title='Blog Post #1',
                            text='Dummy text #1',
                            author=author)
        Post.objects.create(title='Blog Post #2',
                            text='Dummy text #2',
                            author=author)
        Post.objects.create(title='Blog Post #3',
                            text='Dummy text #3',
                            author=author)

    def test_get_all_posts(self):
        # get API response
        response = client.get(reverse('post-list'))
        # get data from db
        posts = Post.objects.all()
        serializer = BlogPostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePostTest(TestCase):
    """ Test module for GET single post API """
    def setUp(self):
        author = User.objects.create(username='test')
        self.post = Post.objects.create(title='Blog Post #1', author=author)

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('post-detail', kwargs={'pk': self.post.pk}))
        post = Post.objects.get(pk=self.post.pk)
        serializer = BlogPostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = client.get(reverse('post-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPostTest(TestCase):
    """ Test module for POST a new post API """
    def setUp(self):
        self.author = User.objects.create(username='test')
        self.valid_payload = {
            'title': 'Blog Post #1',
            'text': 'Blog Post Description',
            'author': 1,
        }
        self.invalid_payload = {
            'title': 'Blog Post #1',
            'author': 2,
        }

    def test_create_valid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_post(self):
        response = client.post(reverse('post-list'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
