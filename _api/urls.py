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
    path('posts/all', views.get_all_posts, name="get-all-posts"),
    path('news/all', views.get_all_news, name="get-all-news"),
    path('posts/query', views.get_posts_query, name="get-posts-query"),
    path('news/query', views.get_news_query, name="get-news-query"),
    path('test/', views.test_api, name="test-api")
]