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
    path('search/', views.search, name='search'),
    path('pointshop/', views.pointshop, name='pointshop'),
    path('<int:icon_id>/<int:icon_price>/buy/', views.icon_buy, name='icon_buy'),
    path('profile/', views.profile, name='profile'),
    path('<int:icon_id>/icon_setting/', views.icon_setting, name='icon_setting'),
    path('<int:article_pk>/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<str:color_name>/<int:color_price>/buy/', views.color_buy, name='color_buy'),
    path('<str:color_name>/color_setting/username', views.color_username, name='color_username'),
    path('<str:color_name>/color_setting/title', views.color_title, name='color_title'),



    

    path('download/', views.download, name='download'),
    path('test/', views.test, name='test'),
    

]