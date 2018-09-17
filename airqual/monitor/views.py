from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import DataPoint, Sensor
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return HttpResponse("index")

@csrf_exempt
def addDataPoint(request):
    #todo here - API key
   
    sensor_id_arg = request.GET.get('sensor_id')
    sensor_object = get_object_or_404(Sensor, sensor_id=sensor_id_arg)
    
    #at this point, we know we have a valid sensor
    
    #construct the datapoint
    val = request.GET.get('value')
    datapoint = DataPoint(value = val, timestamp = timezone.now(), owner=sensor_id_arg)
    datapoint.save()
    #assign the datapoint to the sensor it belongs to
    sensor_object.values.append(datapoint)
    return HttpResponse("added data point")
