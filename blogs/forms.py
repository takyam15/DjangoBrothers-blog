from django import forms

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