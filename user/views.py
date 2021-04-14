from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from newsletter.models import Newsletter

import json

with open("variable.json") as file:
    var = json.load(file)

EMAIL_ADDRESS = var["EMAIL_HOST_USER"]


# Main Homepage for the website
def home(request):
    # print(subscribers)
    return render(request, 'user/homepage.html')


def user_account(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        return render(request, "user/test.html")
    return redirect("homepage")


def login(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome {user.username}, you are now logged in')
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, "user/login.html")


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'You logged out successfully!')
        return redirect('homepage')
    return redirect('homepage')


def about_me(request):
    return render(request, 'user/about.html')


def contact_me(request):
    if request.method == "POST":
        name = request.POST.get("user")
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        message = f"{feedback}\nby {email}"

        subject = f"[BBG] - {name} has sent you a message"

        send_mail(subject=subject, message=message, from_email=EMAIL_ADDRESS,
                  recipient_list=[EMAIL_ADDRESS], fail_silently=True)
        return redirect("contact-me")
    return render(request, 'user/contact-me.html')


def contact_me_success(request):
    pass
