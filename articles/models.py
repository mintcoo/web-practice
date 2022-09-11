from django.db import models

# Create your models here.
class Article(models.Model):
    header_choices = (
	('기타', '기타'),
    ('잡담', '잡담'),
    ('유머', '유머'),
    ('게임', '게임'),
    ('일상', '일상'),
    )
    header = models.CharField(max_length=2, choices=header_choices, default='기타')
    username = models.CharField(default='익명',max_length=50)
    title = models.CharField(max_length=20)
    content = models.TextField()
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    username = models.CharField(default='익명',max_length=50)
    article_id = models.IntegerField(default=0)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    