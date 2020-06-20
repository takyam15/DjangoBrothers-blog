import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Blog


# Create your tests here.

class BlogFactory(factory.django.DjangoModelFactory):
    """Create data for the Blog model used for tests
    """
    title = 'Example title'
    slug = 'example-slug'
    text = 'This is an example text. '
    created_datetime = timezone.now()
    updated_datetime = timezone.now()

    class Meta:
        model = Blog


# Tests for the views

class TestBlogList(TestCase):
    def test_get(self):
        blog_1 = BlogFactory(slug='first-post')
        blog_2 = BlogFactory(slug='second-post')
        res = self.client.get(reverse('blogs:index'))
        blogs = res.context['blog_list']
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(len(blogs), 2)
        self.assertEqual(blogs[0].slug, 'second-post')
        self.assertEqual(blogs[1].slug, 'first-post')


class TestBlogDetail(TestCase):
    def test_get(self):
        blog = BlogFactory(
            title='Sample post',
            slug='post'
        )
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'post'}))
        blog = res.context['blog']
        self.assertTemplateUsed(res, 'blogs/detail.html')
        self.assertEqual(blog.title, 'Sample post')

    def test_404(self):
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'post'}))
        self.assertEqual(res.status_code, 404)
