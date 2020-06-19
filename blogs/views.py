from django.shortcuts import get_object_or_404, render

from .models import Blog


# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/index.html', context)


def detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {'blog': blog}
    return render(request, 'blogs/detail.html', context)