from django.shortcuts import render


def subscribe(request):
    return render(request, "newsletter/subscribe.html")
