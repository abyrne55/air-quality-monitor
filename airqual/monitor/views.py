from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import DataPoint, Sensor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    return render(request, 'monitor/index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            u = user_form.save()
            u.first_name = request.POST['first_name']
            u.last_name = request.POST['last_name']
            u.save()
            return redirect('login')
    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})

def add_data_point(request, sensor_id):
    """
    Adds a DataPoint, authenticating via API key
    """
    # Validate request has necessary fields
    if "api_key" not in request.GET or "value" not in request.GET or sensor_id is None:
        return HttpResponse(status_code=400) # 400 Bad Request

    # Get params
    api_key = request.GET.get('api_key')
    sensor = get_object_or_404(Sensor, id=request.GET.get('sensor_id'))

    # Check API key
    if api_key != str(sensor.api_key):
        return HttpResponse(status_code=403) # 403 Forbidden

    # Now that we know request is valid, construct the datapoint
    sensor.data.create(value=request.GET.get('value'))

    # Return a successful response code
    return HttpResponse(status_code=201) # 201 Created
