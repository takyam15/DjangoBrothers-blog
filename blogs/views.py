from django.db.models import Q
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

    def get_context_data(self):
        context = super().get_context_data()
        context['search_form'] = BlogSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        form = BlogSearchForm(self.request.GET)
        queryset = super().get_queryset()

        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            if keyword:
                queryset = queryset.filter(
                    Q(title__icontains=keyword) | Q(text__icontains=keyword)
                )

        return queryset


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
