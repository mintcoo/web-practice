from django.db import models

# Create your models here.
class Movie(models.Model):
    genre_choices = (
	('기타', '기타'),
    ('액션', '액션'),
    ('공포', '공포'),
    ('로맨스', '로맨스'),
    ('스릴러', '스릴러'),
    )
    genre = models.CharField(max_length=10, choices=genre_choices, default='기타')
    username = models.CharField(default='익명',max_length=16)
    title = models.CharField(max_length=20)
    score = models.FloatField()
    content = models.TextField()
    release_date = models.DateField(auto_now=False)
    count = models.IntegerField(default=0)
    poster_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)