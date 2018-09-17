from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("index")

def addDataPoint(request):
    return HttpResponse("add data point")
