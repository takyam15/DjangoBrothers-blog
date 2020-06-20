from django import forms
from django.db.models import Q

from .models import Blog


class BlogSearchForm(forms.Form):
    keyword = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mr-sm-2',
            'placeholder': '記事を検索'
        }),
        required=False,
    )

    def filter_blogs(self, blogs):

        if self.is_valid():
            keyword = self.cleaned_data.get('keyword')
            if keyword:
                blogs = blogs.filter(
                    Q(title__icontains=keyword) | Q(text__icontains=keyword)
                )

        return blogs