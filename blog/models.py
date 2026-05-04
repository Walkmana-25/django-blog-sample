from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField('タイトル', max_length=100)
    content = models.TextField('本文')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作成者')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿一覧'
        ordering = ['-created_at']
