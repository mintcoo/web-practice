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
    title = models.CharField(max_length=30)
    content = models.TextField()
    count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def 날짜이쁘게(self,date):
        return date.strftime("%Y/%m/%d/ %H:%M:%S")
    
    def 욕필터(self,str):
        return str.replace("씨팔","**")


class Comment(models.Model):
    username = models.CharField(default='익명',max_length=50)
    article_id = models.IntegerField(default=0)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Upcheck(models.Model):
    username = models.CharField(default='익명',max_length=50)
    article_id = models.IntegerField(default=0)


class Usericon(models.Model):
    icon_id = models.IntegerField()
    iconname = models.CharField(max_length=20)
    url = models.TextField()
    price = models.IntegerField(default=500)

class Profile(models.Model):
    username = models.CharField(max_length=50)
    icon_id = models.IntegerField(default=0)
    icon_url = models.TextField(default='icon/gunbbang.png')
    id_color = models.TextField(default='black')
    title_color = models.TextField(default='black')

class Itembox(models.Model):
    username = models.CharField(max_length=50)
    icon_id = models.IntegerField(default=0)
    
class Colorbox(models.Model):
    username = models.CharField(max_length=50)
    color =  models.TextField(default='black')