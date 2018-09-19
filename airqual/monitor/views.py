from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.forms import modelform_factory, HiddenInput
from .models import DataPoint, Sensor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
# Create your views here.

@login_required
def index(request):
    sensors = request.user.sensor_set.all()
    return render(request, 'monitor/index.html', context={'sensor_list' : sensors})

@login_required
def sensor_data(request, sensor_id):
    sensor = get_object_or_404(Sensor, id=sensor_id)
    time_threshold = datetime.now() - timedelta(weeks=1)
    datapoints = sensor.data.filter(timestamp__gt=time_threshold)
    dp_short = datapoints.order_by('-timestamp') if datapoints.count() < 5 else datapoints.order_by('-timestamp')[:5]
    api_key = str(sensor.api_key)
    return render(request, 'monitor/view_sensor.html', context={'sensor' : sensor,
                                                                'datapoints' : datapoints,
                                                                'dp_short' : dp_short,
                                                                'api_key' : api_key})
@login_required
def new_sensor(request):
    SensorForm = modelform_factory(Sensor,
        fields=("name", "unit", "min_value", "max_value", "owner"),
        widgets={"owner": HiddenInput()})
    if request.method == 'POST':
        # Have to do a wierd hack here to set owner data
        post_data = request.POST.copy()
        post_data['owner'] = request.user.id
        sensor_form = SensorForm(post_data)
        if sensor_form.is_valid():
            s = sensor_form.save()
            s.owner = request.user
            s.save()
            return redirect('/monitor/view/' + str(s.id))
    else:
        sensor_form = SensorForm()

    return render(request, 'monitor/new_sensor.html', {'form': sensor_form})

@login_required
def del_sensor(request, sensor_id):
    sensor = get_object_or_404(Sensor, id=sensor_id)
    sensor_name = sensor.name
    if sensor.owner == request.user:
        sensor.delete()
    else:
        return HttpResponse(status=403) # 403 Forbidden

    return render(request, 'monitor/del_sensor.html', {'name': sensor_name})



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
        user_form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': user_form})

def add_data_point(request, sensor_id):
    """
    Adds a DataPoint, authenticating via API key
    """
    # Validate request has necessary fields
    if "api_key" not in request.GET or "value" not in request.GET or sensor_id is None:
        return HttpResponse(status=400) # 400 Bad Request

    # Get params
    api_key = request.GET.get('api_key')
    sensor = get_object_or_404(Sensor, id=sensor_id)

    # Check API key
    if api_key != str(sensor.api_key):
        return HttpResponse(status=403) # 403 Forbidden

    # Now that we know request is valid, construct the datapoint
    datapoint = sensor.data.create(value=request.GET.get('value'))

    # And check if that value was 'sane' (i.e. not a bad sensor)
    if float(datapoint.value) < sensor.min_value or float(datapoint.value) > sensor.max_value:
        sensor.malfunction = True
        sensor.save()

    # Return a successful response code
    return HttpResponse(status=201) # 201 Created
