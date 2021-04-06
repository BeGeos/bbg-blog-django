from django.shortcuts import render, HttpResponse


# Create your views here.
def all_news(request):
    return HttpResponse("<h3>This is the news homepage</h3>")
