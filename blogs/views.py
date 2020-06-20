from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    ListView, DetailView,
)
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
)

from .forms import BlogSearchForm
from .models import Blog
from .serializers import (
    BlogListSerializer, BlogRetrieveSerializer,
)


# Create your views here.

class BlogList(ListView):
    model = Blog
    template_name = 'blogs/index.html'
    paginate_by = 10

    def get_queryset(self):
        form = BlogSearchForm(self.request.GET)
        queryset = super().get_queryset()
        queryset = form.filter_blogs(queryset)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context['search_form'] = BlogSearchForm(self.request.GET)
        return context


class BlogDetail(DetailView):
    model = Blog
    template_name = 'blogs/detail.html'


class BlogListAPI(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer


class BlogRetrieveAPI(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogRetrieveSerializer
    lookup_field = 'slug'
