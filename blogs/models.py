from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Author(AbstractUser):
    pass


class Blog(models.Model):
    title = models.CharField('タイトル', max_length=150)
    slug = models.SlugField('スラッグ')
    text = models.TextField('本文', blank=True)
    created_datetime = models.DateTimeField('作成日', auto_now_add=True)
    updated_datetime = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        ordering = ('-created_datetime',)

    def __str__(self):
        return self.title