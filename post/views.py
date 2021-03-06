from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import get_token

from .models import Post, PostTag
from .forms import PostBodyForm

import re
import json
import requests

with open("variable.json") as file:
    var = json.load(file)


# Inner backend logic
def slug_gen(title):
    title = title.strip()
    return re.sub(r'\W+|\s+|_', "-", title).lower()


def parse_tags(tags):
    tags = tags.strip()
    return re.split(r',\s*', tags)


def all_posts(request):
    order = request.session.get("order-post", default="created_on")
    # print(request.session.items())
    if not order:
        order = "created_on"
    if order == "date":
        order = "created_on"

    posts = Post.objects.order_by(f'-{order}', "-created_on").all()
    context = {
        "posts": posts,
    }

    return render(request, "post/all-posts.html", context)


def create_post(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = PostBodyForm()

        if request.method == "POST":
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            text = request.POST.get('post')
            img = request.FILES.get("thumbnail")
            new_post = Post.objects.create(
                title=title,
                summary=summary,
                post=text,
                author=request.user.username,
                image=img,
                slug=slug_gen(title)
            )

            tags = parse_tags(request.POST.get("tags"))
            for tag in tags:
                PostTag.objects.create(post_id=new_post, tag=tag)

            data = {
                "title": new_post.title,
                "summary": new_post.summary,
                "link": var["BASE_URL"] + f"blog/post/{new_post.slug}"
            }

            csrf_token = get_token(request)
            cookies = {"csrftoken": csrf_token}
            # print(csrf_token)
            headers = {"X-CSRFToken": csrf_token}

            # Send Email via API call
            # requests.post(var["BASE_URL"] + "_api/send-notification/",
            #               json=data, headers=headers, cookies=cookies)

            messages.success(request, 'Your new post was created successfully!')
            return redirect("all-posts")

        return render(request, 'post/create-post.html', context={"form": form})

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-posts')


def update_post(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        post = get_object_or_404(Post, slug=slug)
        tags = PostTag.objects.filter(post_id=post)
        tag_string = ", ".join([tag.tag for tag in tags])
        tags.delete()
        if request.method == "POST":
            post.title = request.POST.get("title")
            post.summary = request.POST.get("summary")
            post.post = request.POST.get("post")
            if request.FILES.get("thumbnail"):
                post.image = request.FILES.get("thumbnail")
            post.save()

            tags = parse_tags(request.POST.get("tags"))
            for tag in tags:
                PostTag.objects.create(post_id=post, tag=tag)

            messages.success(request, "The post was updated successfully!")
            return redirect('all-posts')

        context = {
            "post": post,
            "tags": tag_string
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
