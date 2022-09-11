from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    # path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>', views.detail, name='detail'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    # path('<int:article_pk>/edit/', views.edit, name='edit'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/comment', views.comment, name='comment'),
    path('<int:article_pk>/upcount', views.upcount, name='upcount'),
    

    path('download/', views.download, name='download'),
    path('test/', views.test, name='test'),
    

]