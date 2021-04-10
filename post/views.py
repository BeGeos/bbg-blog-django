from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Post, PostImage, PostTag

import re


# Inner backend logic
def slug_gen(title):
    return re.sub(r'\W+|\s+|_', "-", title).lower()


def parse_tags(tags):
    return re.split(r',\s*', tags)


def all_posts(request):
    posts = Post.objects.order_by('-created_on').all()
    context = {
        "posts": posts,
    }

    return render(request, "post/all-posts.html", context)


def create_post(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            text = request.POST.get('text-post')
            new_post = Post.objects.create(
                title=title,
                summary=summary,
                post=text,
                author=request.user.username,
                slug=slug_gen(title)
            )

            tags = parse_tags(request.POST.get("tags"))
            for tag in tags:
                PostTag.objects.create(post_id=new_post, tag=tag)

            messages.success(request, 'Your new post was created successfully!')
            return redirect("all-posts")

        return render(request, 'post/create-post.html')

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-posts')


def update_post(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
        if request.method == "POST":
            post.title = request.POST.get("title")
            post.summary = request.POST.get("summary")
            post.post = request.POST.get("text-post")
            post.save()
            messages.success(request, "The post was updated successfully!")
            return redirect('all-posts')

        context = {
            "post": post
        }
        return render(request, 'post/update-post.html', context)

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-posts')


def delete_post(request, slug):
    """Delete logic, then redirect"""
    if request.user.is_authenticated and request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
        # post = Post.objects.filter(slug=slug).first()
        post.delete()
        messages.success(request, 'The post was deleted successfully!')
        return redirect('all-posts')

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-posts')


def single_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.order_by('-created_on')[:3]
    context = {
        "post": post,
        "recent_posts": recent_posts
    }
    return render(request, 'post/single-post.html', context)
