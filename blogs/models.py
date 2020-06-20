from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Author(AbstractUser):
    pass


class Blog(models.Model):
<<<<<<< HEAD
    title = models.CharField('タイトル', blank=False, null=False, max_length=150)
=======
    title = models.CharField('タイトル', max_length=150)
    slug = models.SlugField('スラッグ')
>>>>>>> origin/master
    text = models.TextField('本文', blank=True)
    created_datetime = models.DateTimeField('作成日', auto_now_add=True)
    updated_datetime = models.DateTimeField('更新日', auto_now=True)

<<<<<<< HEAD
=======
    class Meta:
        ordering = ('-created_datetime',)

>>>>>>> origin/master
    def __str__(self):
        return self.title