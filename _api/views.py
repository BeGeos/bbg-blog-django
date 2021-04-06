from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def home_api(request):
    return JsonResponse({"message": "This is the home api"})
