from django.shortcuts import render, redirect, get_object_or_404
from django.middleware.csrf import get_token
from django.contrib import messages

from .models import News, NewsImage, NewsTag

import re
import json
import requests

with open("variable.json") as file:
    var = json.load(file)


# Inner backend logic
def slug_gen(title):
    return re.sub(r'\W+|\s+|_', "-", title).lower()


def parse_tags(tags):
    return re.split(r',\s*', tags)


# Main routes
def all_news(request):
    news = News.objects.order_by('-created_on').all()
    context = {
        "news": news,
    }

    return render(request, "news/all-news.html", context)


def create_news(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            text = request.POST.get('text-news')
            new_news = News.objects.create(
                title=title,
                summary=summary,
                news=text,
                author=request.user.username,
                slug=slug_gen(title)
            )

            tags = parse_tags(request.POST.get("tags"))
            for tag in tags:
                NewsTag.objects.create(post_id=new_news, tag=tag)

            # TODO Send notification to subscribers
            data = {
                    "title": new_news.title,
                    "summary": new_news.summary,
                    "link": var["BASE_URL"] + f"news/article/{new_news.slug}"
                   }

            csrf_token = get_token(request)
            cookies = {"csrftoken": csrf_token}
            # print(csrf_token)
            headers = {"X-CSRFToken": csrf_token}

            requests.post(var["BASE_URL"] + "_api/send-notification/",
                          json=data, headers=headers, cookies=cookies)

            messages.success(request, 'Your new article was created successfully!')
            return redirect("all-news")

        return render(request, 'news/create-news.html')

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-news')


def single_news(request, slug):
    news = get_object_or_404(News, slug=slug)
    recent_news = News.objects.order_by('-created_on')[:3]
    context = {
        "news": news,
        "recent_news": recent_news
    }
    return render(request, 'news/single-news.html', context)


def update_news(request, slug):
    if request.user.is_authenticated and request.user.is_superuser:
        news = get_object_or_404(News, slug=slug)
        if request.method == "POST":
            news.title = request.POST.get("title")
            news.summary = request.POST.get("summary")
            news.news = request.POST.get("text-news")
            news.save()
            messages.success(request, "The article was updated successfully!")
            return redirect('all-news')

        context = {
            "news": news
        }
        return render(request, 'news/update-news.html', context)

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-news')


def delete_news(request, slug):
    """Delete logic, then redirect"""
    if request.user.is_authenticated and request.user.is_superuser:
        news = get_object_or_404(News, slug=slug)
        news.delete()
        messages.success(request, 'The article was deleted successfully!')
        return redirect('all-news')

    messages.info(request, 'You need to be logged in, champ!')
    return redirect('all-news')
