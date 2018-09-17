from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import DataPoint

# Create your views here.

def index(request):
    return HttpResponse("index")

def addDataPoint(request):
    datapoint = DataPoint.objects.create(value = 1, timestamp = timezone.now())
    return HttpResponse("add data point")
