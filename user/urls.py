from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_account, name="account"),
    path('about/', views.about_me, name="about-me"),
    path('contact-me/', views.contact_me, name="contact-me"),
    path('contact-me/success', views.contact_me_success, name="contact-me-success"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]