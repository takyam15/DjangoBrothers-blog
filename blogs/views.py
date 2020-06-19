from django.shortcuts import render

from .models import Blog


# Create your views here.

def index(request):
    blogs = Blog.objects.order_by('-created_datetime')
    context = {'blogs': blogs}
    return render(request, 'blogs/index.html', context)


def detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    context = {'blog': blog}
    return render(request, 'blogs/detail.html', context)