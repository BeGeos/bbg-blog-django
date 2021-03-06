from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.all_posts, name="all-posts"),
    path('create-post/', views.create_post, name="create-post"),
    path('update-post/<slug>', views.update_post, name="update-post"),
    path('post/<slug>', views.single_post, name="single-post"),
    path('delete/<slug>', views.delete_post, name="delete-post")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
