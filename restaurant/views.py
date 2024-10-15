from django.shortcuts import render
from django.http import HttpResponse

def restaurant(request):
    return HttpResponse("Hello, world.")
