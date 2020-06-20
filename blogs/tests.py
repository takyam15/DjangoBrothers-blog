import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import BlogSearchForm
from .models import Blog


# Create your tests here.

class BlogFactory(factory.django.DjangoModelFactory):
    """Create data for the Blog model used for tests"""
    title = 'Example title'
    slug = 'example-slug'
    text = 'This is an example text.'
    created_datetime = timezone.now()
    updated_datetime = timezone.now()

    class Meta:
        model = Blog


# Tests for the forms

class TestBlogSearchForm(TestCase):
    def test_filter_blogs(self):
        blog_1 = BlogFactory(
            title='First post', slug='first-post', text='This blog is opened.'
        )
        blog_2 = BlogFactory(
            title='Second post', slug='second-post', text='This is the second post.'
        )
        blog_3 = BlogFactory(
            title='Third post', slug='third-post', text='This is not the first post.'
        )
        blog_4 = BlogFactory(
            title='Dummy first post', slug='forth-post', text='This is the forth post.'
        )
        blog_5 = BlogFactory(
            title='Draft post', slug='fifth-post', text='The First post has been withdrawn.'
        )
        form = BlogSearchForm({'keyword': 'first'})
        blogs = form.filter_blogs(Blog.objects.all())
        self.assertEqual(len(blogs), 4)
        self.assertEqual(blogs[0].text, 'The First post has been withdrawn.')
        self.assertEqual(blogs[1].title, 'Dummy first post')
        self.assertEqual(blogs[2].text, 'This is not the first post.')
        self.assertEqual(blogs[3].title, 'First post')

    def test_not_filter_blogs(self):
        blog_1 = BlogFactory(slug='first-post')
        blog_2 = BlogFactory(slug='second-post')
        form = BlogSearchForm({'keyword': ''})
        blogs = form.filter_blogs(Blog.objects.all())
        self.assertEqual(len(blogs), 2)


# Tests for the views

class TestBlogList(TestCase):
    def test_get(self):
        res = self.client.get(reverse('blogs:index'))
        self.assertTemplateUsed(res, 'blogs/index.html')

    def test_get_queryset(self):
        blog_1 = BlogFactory(slug='first-post')
        blog_2 = BlogFactory(slug='second-post')
        blogs = Blog.objects.all()
        self.assertEqual(len(blogs), 2)

    def test_get_context_data(self):
        blog_1 = BlogFactory(slug='first-post')
        blog_2 = BlogFactory(slug='second-post')
        res = self.client.get(reverse('blogs:index'))
        blogs = res.context['blog_list']
        form = res.context['search_form']
        self.assertEqual(len(blogs), 2)
        self.assertIsNotNone(form)


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
