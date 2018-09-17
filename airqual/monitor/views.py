from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import DataPoint, Sensor
# Create your views here.

def index(request):
    return HttpResponse("index")

def addDataPoint(request):
    #very secure
    api_key = request.GET.get('api_key')
    if (api_key != 'complicatedstring'):
        return HttpResponse("Invalid API key")
   
    sensor_id_arg = request.GET.get('sensor_id')
    sensor_object = get_object_or_404(Sensor, sensor_id=sensor_id_arg)
    
    #at this point, we know we have a valid sensor and sensor_id
    
    #construct the datapoint
    val = request.GET.get('value')
    sensor_object.data.create(value=val, timestamp=timezone.now())
    
    return HttpResponse("added data point")
