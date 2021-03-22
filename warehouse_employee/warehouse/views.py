from django.http import HttpResponse
from django.shortcuts import render   # noqa: F401


def index(request):
    return HttpResponse("Hello, world the second project!!!!")
