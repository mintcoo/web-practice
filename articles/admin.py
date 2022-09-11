from django.contrib import admin
from .models import Article

# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')

admin.site.register(Article, Admin)
