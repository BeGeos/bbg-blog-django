from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_news, name="all-news"),
    path('create-news/', views.create_news, name="create-news"),
    path('update-news/<slug>', views.update_news, name="update-news"),
    path('article/<slug>', views.single_news, name="single-news"),
    path('delete/<slug>', views.delete_news, name="delete-news")
]