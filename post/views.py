from django.shortcuts import render, HttpResponse
from django.contrib import messages


def all_posts(request):
    return render(request, "post/all-posts.html")


def create_post(request):
    return render(request, 'post/create-post.html')


def update_post(request, slug):
    return render(request, 'post/update-post.html')


def delete_post(request, slug):
    """Delete logic, then redirect"""
    return render(request, 'post/create-post.html')


def single_post(request, slug):
    return render(request, 'post/single-post.html')
