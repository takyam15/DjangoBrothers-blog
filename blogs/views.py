from django.shortcuts import get_object_or_404, render
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)

from .models import Blog
from .serializers import (
    BlogListSerializer, BlogRetrieveSerializer,
)


# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blogs/index.html', context)


def detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {'blog': blog}
    return render(request, 'blogs/detail.html', context)


class BlogListAPI(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer


class BlogRetrieveAPI(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogRetrieveSerializer
    lookup_field = 'slug'
