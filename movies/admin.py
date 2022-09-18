from django.contrib import admin
from .models import Movie
# Register your models here.
class Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')


admin.site.register(Movie, Admin)