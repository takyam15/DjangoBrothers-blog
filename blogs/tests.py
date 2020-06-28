import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

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

class BlogSearchFormTests(TestCase):
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
        self.assertEqual(Blog.objects.count(), 5)
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
        self.assertEqual(Blog.objects.count(), 2)
        self.assertEqual(len(blogs), 2)


# Tests for the views

class BlogListTests(TestCase):
    def test_get_single_blog(self):
        blog = BlogFactory(title='Single post')
        res = self.client.get(reverse('blogs:index'))
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 1)
        self.assertQuerysetEqual(
            res.context['blog_list'],
            ['<Blog: Single post>']
        )
        self.assertIsNotNone(res.context['search_form'])

    def test_get_two_blogs(self):
        blog_1 = BlogFactory(title='First post', slug='first-post')
        blog_2 = BlogFactory(title='Second post', slug='second-post')
        res = self.client.get(reverse('blogs:index'))
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 2)
        self.assertQuerysetEqual(
            res.context['blog_list'],
            ['<Blog: Second post>', '<Blog: First post>']
        )
        self.assertIsNotNone(res.context['search_form'])

    def test_get_empty_blog(self):
        res = self.client.get(reverse('blogs:index'))
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 0)
        self.assertContains(res, '表示する記事がありません。')
        self.assertQuerysetEqual(
            res.context['blog_list'],
            []
        )
        self.assertIsNotNone(res.context['search_form'])

    def test_get_paginate(self):
        blog_1 = BlogFactory(slug='post-1')
        blog_2 = BlogFactory(slug='post-2')
        blog_3 = BlogFactory(slug='post-3')
        blog_4 = BlogFactory(slug='post-4')
        blog_5 = BlogFactory(slug='post-5')
        blog_6 = BlogFactory(slug='post-6')
        blog_7 = BlogFactory(slug='post-7')
        blog_8 = BlogFactory(slug='post-8')
        blog_9 = BlogFactory(slug='post-9')
        blog_10 = BlogFactory(slug='post-10')
        blog_11 = BlogFactory(slug='post-11')
        res_1 = self.client.get(reverse('blogs:index'), data={'page': 1})
        res_2 = self.client.get(reverse('blogs:index'), data={'page': 2})
        self.assertTemplateUsed(res_1, 'blogs/index.html')
        self.assertTemplateUsed(res_2, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 11)
        self.assertContains(res_1, 'post-11')
        self.assertContains(res_1, 'post-2')
        self.assertContains(res_2, 'post-1')

    def test_get_invalid_page(self):
        blog = BlogFactory()
        res = self.client.get(reverse('blogs:index'), data={'page': 'invalid'})
        self.assertEqual(res.status_code, 404)

    def test_get_invalid_page_number(self):
        blog = BlogFactory()
        res = self.client.get(reverse('blogs:index'), data={'page': 2})
        self.assertEqual(res.status_code, 404)


class BlogDetailTests(TestCase):
    def test_get(self):
        blog = BlogFactory(title='Example post', slug='post')
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'post'}))
        self.assertTemplateUsed(res, 'blogs/detail.html')
        self.assertEqual(res.context['blog'].title, 'Example post')

    def test_404(self):
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'post'}))
        self.assertEqual(res.status_code, 404)


class BlogListAPITests(APITestCase):
    def test_get_blogs_api(self):
        blog_1 = BlogFactory(title='First post', slug='first-post')
        blog_2 = BlogFactory(title='Second post', slug='second-post')
        res = self.client.get(reverse('blogs:api_index'), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.count(), 2)


class BlogRetrieveAPITests(APITestCase):
    def test_get_blog_api(self):
        blog = BlogFactory(title='Example post', slug='post')
        res = self.client.get(reverse('blogs:api_detail', kwargs={'slug': 'post'}), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.context['blog'].title, 'Example post')
