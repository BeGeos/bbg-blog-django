from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_api, name="home-api"),
    path('newsletter/subscribe', views.subscribe, name="subscribe"),
    path('post/like/<slug>', views.add_post_likes, name="add-post-like"),
    path('news/like/<slug>', views.add_news_likes, name="add-news-like"),
    path('post/views/<slug>', views.add_post_views, name="add-post-views"),
    path('news/views/<slug>', views.add_news_views, name="add-news-views"),
    path('send-notification/', views.send_notification_email, name="notification-email"),
]