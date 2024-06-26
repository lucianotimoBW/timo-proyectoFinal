from django.test import TestCase
from .models import Blog
from django.contrib.auth.models import User

class BlogTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        Blog.objects.create(title='Test Blog', subtitle='Test Subtitle', body='Test Body', author=user)

    def test_blog_creation(self):
        blog = Blog.objects.get(title='Test Blog')
        self.assertEqual(blog.subtitle, 'Test Subtitle')
