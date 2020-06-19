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


class TestIndex(TestCase):
    def test_get(self):
        blog_1 = BlogFactory()
        blog_2 = BlogFactory()
        res = self.client.get(reverse('blogs:index'))
        blogs = res.context['blogs']
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(len(blogs), 2)
