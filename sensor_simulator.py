#!/usr/bin/env python3
"""
AirQual Sensor Simulator

Randomly pings the API, adding datapoints
"""
from time import sleep
from urllib.request import urlopen
from random import seed, uniform, choice, randint

# Connection Settings
PROTO = "http"
HOST = "127.0.0.1:8000"

# Sensor Settings
# format: {'sensor_id':'api_key'}
SENSORS = {
        '1':'3999f01e-b85c-4f38-8c28-3f67c89765b8',
        '2':'ec628b76-4013-4e81-933d-9be92be9dd3d',
        '5':'65fbf1eb-8378-4a04-8588-10d9054a9538'
}
VALUE_MIN = 0.0
VALUE_MAX = 100.0

# Delay Settings (seconds)
WAIT_TIME_MIN = 5
WAIT_TIME_MAX = 30

URL = "{}://{}/monitor/add/".format(PROTO, HOST)

def call_api(sensor_id, api_key, value):
    """
    Make the API call to add a DataPoint to the sensor
    """
    call_url = URL + "{}?api_key={}&value={:.2f}".format(sensor_id, api_key, value)

    with urlopen(call_url) as r:
        status_code = r.getcode()
        print("Request to {} replied with HTTP code {}".format(call_url, status_code))

    return status_code

# Seed the RNG
seed()

# Main Loop
while True:
    # Make call
    sid = choice(list(SENSORS.keys()))
    call_api(sensor_id=sid, api_key=SENSORS[sid], value=uniform(VALUE_MIN, VALUE_MAX))

    # Wait
    sleep_time = randint(WAIT_TIME_MIN, WAIT_TIME_MAX)
    print("Waiting {} seconds...".format(sleep_time))
    sleep(sleep_time)
