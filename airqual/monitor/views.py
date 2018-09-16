from django.template import loader
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Question, DataPoint


def index(request):
    if request.method == 'POST':
        return HttpResponse('POST request')

    else:
        return HttpResponse('GET request')

# TODO - get info from request into datapoint
def addDataPoint
    if request.method == 'POST':
        datapoint = DataPoint.objects.create(sensor="test", value=5)
        return HttpResponse('POST to add datapoint')
