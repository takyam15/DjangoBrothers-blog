from rest_framework import serializers

from .models import Blog


class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        exclude = ('text',)


class BlogRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'