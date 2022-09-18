from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.movies, name='movies'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>', views.detail, name='detail'),
]