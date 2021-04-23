from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .serializer import PostSerializer, NewsSerializer

from newsletter.models import Newsletter
from post.models import Post, PostTag
from news.models import News, NewsTag

import json

with open("variable.json") as file:
    var = json.load(file)

EMAIL_ADDRESS = var["EMAIL_HOST_USER"]


# Body parser for JSON data
def body_parser(data):
    body = data.decode("utf-8")
    return json.loads(body)  # Returns the body as JSON


@require_http_methods(["GET"])
def home_api(request):
    return JsonResponse({"message": "This is the home api"})


# Add subscription to Newsletter
@require_http_methods(["POST"])
def subscribe(request):
    data = body_parser(request.body)
    email = data.get("email")

    # Check if email address already exists
    exists = Newsletter.objects.filter(email=email).first()

    if not exists:
        new_sub = Newsletter.objects.create(email=email)

        subject = "[BBG] - New Subscription"
        message = f"Hello There\nThis message is only to confirm your subscription to " \
                  f"the BlockBusterGirl blog.\n\nI am very happy to have you on board.\n" \
                  f"If you have any questions, or preferences or comments don't hesitate to " \
                  f"hit the contact me page.\n\n@BBG"

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=EMAIL_ADDRESS,
            to=[new_sub.email]
        )
        email.send(fail_silently=True)

        return JsonResponse({"message": "New Subscription added!"}, status=200)
    return JsonResponse({"message": "This address already exists"}, status=400)


# Add likes to post and news
@require_http_methods(["POST"])
def add_post_likes(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)
        post.likes += 1
        post.save()
        # print(request.headers)
        return JsonResponse({"likes": post.likes}, status=200)
    except Exception as e:
        return JsonResponse({"message": e}, status=500)


@require_http_methods(["POST"])
def add_news_likes(request, slug):
    try:
        news = get_object_or_404(News, slug=slug)
        news.likes += 1
        news.save()
        return JsonResponse({"likes": news.likes}, status=200)
    except Exception as e:
        return JsonResponse({"message": e}, status=500)


# Add views to post and news
@require_http_methods(["POST"])
def add_post_views(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)
        post.views += 1
        post.save()
        return JsonResponse({"message": "Updated"}, status=200)
    except Exception as e:
        return JsonResponse({"message": e}, status=500)


@require_http_methods(["POST"])
def add_news_views(request, slug):
    try:
        news = get_object_or_404(News, slug=slug)
        news.views += 1
        news.save()
        return JsonResponse({"message": "Updated"}, status=200)
    except Exception as e:
        return JsonResponse({"message": e}, status=500)


# Send Email API
@require_http_methods(["POST"])
def send_notification_email(request):
    # data = body_parser(request.body)
    # subscribers = Newsletter.objects.filter(active=True)
    # recipients = []  # Array of email addresses
    # for each in subscribers:
    #     recipients.append(each.email)
    #
    # context = {
    #     "article": data
    # }
    #
    # subject = "[BBG] - New article out!"
    # html_message = render_to_string("_api/notification-email.html", context)
    # plain_message = strip_tags(html_message)
    #
    # email = EmailMultiAlternatives(
    #     subject=subject,
    #     body=plain_message,
    #     from_email=EMAIL_ADDRESS,
    #     to=[EMAIL_ADDRESS],
    #     bcc=recipients
    # )
    #
    # email.attach_alternative(html_message, "text/html")
    # email.send(fail_silently=True)

    return JsonResponse({"message": "Accepted"}, status=200)


# Get all posts or news
@require_http_methods(["GET"])
def get_all_posts(request):
    all_posts = Post.objects.all()
    order = request.GET.get('order')
    request.session.__setitem__("order-post", order)
    data = ""  # In case nothing come back

    if not order or order == "date":
        data = all_posts.order_by("-created_on")

    if order == "views":
        data = all_posts.order_by("-views", "-created_on")

    if order == "likes":
        data = all_posts.order_by("-likes", "-created_on")

    serializer = PostSerializer(instance=data, many=True)

    return JsonResponse({"data": serializer.data}, status=200)


@require_http_methods(["GET"])
def get_all_news(request):
    all_news = News.objects.all()
    order = request.GET.get('order')
    request.session.__setitem__("order-news", order)
    # print(order)
    data = ""  # In case nothing comes back

    if not order or order == "date":
        data = all_news.order_by("-created_on")

    if order == "views":
        data = all_news.order_by("-views", "-created_on")

    if order == "likes":
        data = all_news.order_by("-likes", "-created_on")

    serializer = NewsSerializer(instance=data, many=True)

    return JsonResponse({"data": serializer.data}, status=200)


def get_posts_query(request):
    order = request.session.get("order-post", default="created_on")
    if order == "date":
        order = "created_on"

    query = request.GET.get("q")
    tag = request.GET.get("tag")
    entries = ""
    if query:
        entries = Post.objects.filter(title__icontains=query).order_by(f"-{order}")
    elif tag:
        inner_qs = PostTag.objects.filter(tag__iexact=tag).values("post_id")
        entries = Post.objects.filter(id__in=inner_qs).order_by(f"-{order}")

    serializer = PostSerializer(instance=entries, many=True)
    return JsonResponse({"data": serializer.data})


def get_news_query(request):
    order = request.session.get("order-post", default="created_on")
    if order == "date":
        order = "created_on"

    query = request.GET.get("q")
    tag = request.GET.get("tag")
    entries = ""
    if query:
        entries = News.objects.filter(title__icontains=query).order_by(f"-{order}")
    elif tag:
        inner_qs = NewsTag.objects.filter(tag__iexact=tag).values("post_id")
        entries = News.objects.filter(id__in=inner_qs).order_by(f"-{order}")

    serializer = NewsSerializer(instance=entries, many=True)
    return JsonResponse({"data": serializer.data})


# Debugging
@api_view(("GET",))
@renderer_classes([JSONRenderer])
def test_api(request):
    order = request.session.get("order-post", default="created_on")
    tag = request.GET.get("tag")
    inner_qs = PostTag.objects.filter(tag__iexact=tag).values("post_id")
    entries = Post.objects.filter(id__in=inner_qs)
    serializer = PostSerializer(instance=entries, many=True)

    return Response(serializer.data, status=200)
    # return JsonResponse({"message": serializer.data})
