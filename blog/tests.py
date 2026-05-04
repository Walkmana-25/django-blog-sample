from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Content')

    def test_post_create_view_unauthenticated(self):
        response = self.client.get(reverse('post_create'))
        self.assertNotEqual(response.status_code, 200) # Should redirect to login

    def test_post_create_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_update_view_author(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post_update', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_update_view_not_author(self):
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(reverse('post_update', args=[self.post.id]))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_post_delete_view_author(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view_not_author(self):
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(reverse('post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
