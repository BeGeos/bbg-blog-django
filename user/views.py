from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


# Main Homepage for the website
def home(request):
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
    return render(request, 'user/contact-me.html')
