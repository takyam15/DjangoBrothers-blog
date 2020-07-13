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
    title = 'Example blog'
    slug = 'example-blog'
    text = 'This is an example blog.'
    created_datetime = timezone.now()
    updated_datetime = timezone.now()

    class Meta:
        model = Blog


# Tests for the forms

class BlogSearchFormTests(TestCase):

    def test_filter_blogs(self):
        blog_1 = BlogFactory(
            title='First blog', slug='first-blog', text='This blog is opened.'
        )
        blog_2 = BlogFactory(
            title='Second blog', slug='second-blog', text='This is the second blog.'
        )
        blog_3 = BlogFactory(
            title='Third blog', slug='third-blog', text='This is not the first blog.'
        )
        blog_4 = BlogFactory(
            title='Dummy first blog', slug='forth-blog', text='This is the forth blog.'
        )
        blog_5 = BlogFactory(
            title='Draft blog', slug='fifth-blog', text='The First blog has been withdrawn.'
        )
        form = BlogSearchForm({'keyword': 'first'})
        blogs = form.filter_blogs(Blog.objects.all())
        self.assertEqual(Blog.objects.count(), 5)
        self.assertEqual(blogs.count(), 4)
        self.assertEqual(blogs[0].text, 'The First blog has been withdrawn.')
        self.assertEqual(blogs[1].title, 'Dummy first blog')
        self.assertEqual(blogs[2].text, 'This is not the first blog.')
        self.assertEqual(blogs[3].title, 'First blog')

    def test_not_filter_blogs(self):
        blog_1 = BlogFactory(slug='first-blog')
        blog_2 = BlogFactory(slug='second-blog')
        form = BlogSearchForm({'keyword': ''})
        blogs = form.filter_blogs(Blog.objects.all())
        self.assertEqual(Blog.objects.count(), 2)
        self.assertEqual(blogs.count(), 2)


# Tests for the views

class BlogListTests(TestCase):

    def test_get_blog_list(self):
        blog_1 = BlogFactory(title='First blog', slug='first-blog')
        blog_2 = BlogFactory(title='Second blog', slug='second-blog')
        res = self.client.get(reverse('blogs:index'))
        self.assertTemplateUsed(res, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 2)
        self.assertQuerysetEqual(
            res.context['blog_list'],
            ['<Blog: Second blog>', '<Blog: First blog>']
        )
        self.assertIsNotNone(res.context['search_form'])

    def test_get_empty_blog_list(self):
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
        blog_1 = BlogFactory(
            title='Blog 1',
            slug='blog-1'
        )
        blog_2 = BlogFactory(
            title='Blog 2',
            slug='blog-2'
        )
        blog_3 = BlogFactory(
            title='Blog 3',
            slug='blog-3'
        )
        blog_4 = BlogFactory(
            title='Blog 4',
            slug='blog-4'
        )
        blog_5 = BlogFactory(
            title='Blog 5',
            slug='blog-5'
        )
        blog_6 = BlogFactory(
            title='Blog 6',
            slug='blog-6'
        )
        blog_7 = BlogFactory(
            title='Blog 7',
            slug='blog-7'
        )
        blog_8 = BlogFactory(
            title='Blog 8',
            slug='blog-8'
        )
        blog_9 = BlogFactory(
            title='Blog 9',
            slug='blog-9'
        )
        blog_10 = BlogFactory(
            title='Blog 10',
            slug='blog-10'
        )
        blog_11 = BlogFactory(
            title='Blog 11',
            slug='blog-11'
        )
        res_page_1 = self.client.get(reverse('blogs:index'), data={'page': 1})
        res_page_2 = self.client.get(reverse('blogs:index'), data={'page': 2})
        self.assertTemplateUsed(res_page_1, 'blogs/index.html')
        self.assertTemplateUsed(res_page_2, 'blogs/index.html')
        self.assertEqual(Blog.objects.count(), 11)
        self.assertQuerysetEqual(
            res_page_1.context['blog_list'],
            [
                '<Blog: Blog 11>',
                '<Blog: Blog 10>',
                '<Blog: Blog 9>',
                '<Blog: Blog 8>',
                '<Blog: Blog 7>',
                '<Blog: Blog 6>',
                '<Blog: Blog 5>',
                '<Blog: Blog 4>',
                '<Blog: Blog 3>',
                '<Blog: Blog 2>',
            ]
        )
        self.assertQuerysetEqual(
            res_page_2.context['blog_list'],
            ['<Blog: Blog 1>']
        )

    def test_get_non_existent_page_number(self):
        blog = BlogFactory()
        res = self.client.get(reverse('blogs:index'), data={'page': 2})
        self.assertEqual(res.status_code, 404)

    def test_get_string_page_number(self):
        blog = BlogFactory()
        res = self.client.get(reverse('blogs:index'), data={'page': 'string'})
        self.assertEqual(res.status_code, 404)


class BlogDetailTests(TestCase):

    def test_get_blog(self):
        blog = BlogFactory(title='Sample blog', slug='sample-blog')
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'sample-blog'}))
        self.assertTemplateUsed(res, 'blogs/detail.html')
        self.assertEqual(res.context['blog'].title, 'Sample blog')

    def test_get_non_existent_blog(self):
        res = self.client.get(reverse('blogs:detail', kwargs={'slug': 'sample-blog'}))
        self.assertEqual(res.status_code, 404)


class BlogListAPITests(APITestCase):

    def test_get_blogs_api(self):
        blog_1 = BlogFactory(title='First blog', slug='first-blog')
        blog_2 = BlogFactory(title='Second blog', slug='second-blog')
        res = self.client.get(reverse('blogs:api_index'), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Blog.objects.count(), 2)


class BlogRetrieveAPITests(APITestCase):

    def test_get_blog_api(self):
        blog = BlogFactory(title='Sample blog', slug='sample-blog')
        res = self.client.get(reverse('blogs:api_detail', kwargs={'slug': 'sample-blog'}), format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
