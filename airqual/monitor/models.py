from django.db import models
from django.utils import timezone
import datetime


# Create your models here.

# Data point model - to be created by POST requests by sensor
class DataPoint(models.Model):
    sensor = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    #timestamp = models.DateTimeField('timestamp')
    def __str__(self):
        return self.value

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    curr_value = models.IntegerField(default=0)
    def __str__(self):
        return self.name

