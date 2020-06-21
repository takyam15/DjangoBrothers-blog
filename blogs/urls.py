"""blogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    BlogList, BlogDetail, BlogListAPI, BlogRetrieveAPI,
)

app_name = 'blogs'
urlpatterns = [
    path('', BlogList.as_view(), name='index'),
    path('<slug:slug>/', BlogDetail.as_view(), name='detail'),
    path('api/posts/', BlogListAPI.as_view(), name='api_index'),
    path('api/posts/<slug:slug>/', BlogRetrieveAPI.as_view(), name='api_detail'),
]