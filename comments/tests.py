from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Rate


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post', content='Test Content')
        self.post_content_type = ContentType.objects.get_for_model(Post)
        self.comment = Comment.objects.create(user=self.user, content='Test Comment', object_id=self.post.id,
                                              content_type=self.post_content_type)

    def test_add_rating(self):
        client = APIClient()
        client.force_authenticate(user=self.user)

        comment = Comment.objects.create(
            user=self.user, content='Test Comment', parent=self.comment)
        second = Comment.objects.create(
            user=self.user, content='Test Comment', parent=comment)
        third = Comment.objects.create(
            user=self.user, content='Test Comment', parent=second)

        data = {'rating': 1}

        response = client.post(
            f'/comment/{comment.id}/add_rating/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.post(
            f'/comment/{comment.id}/add_rating/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rate.objects.count(), 1)
        client.post(
            f'/comment/{second.id}/add_rating/', data, format='json')
        client.post(
            f'/comment/{third.id}/add_rating/', data, format='json')

        response = client.get(f'/comments/{comment.id}/')

        thread_rating = response.data.get('thread_rating')
        comment_rating = response.data.get('comment_rating')

        self.assertEqual(thread_rating, 3)
        self.assertEqual(comment_rating, 1)
