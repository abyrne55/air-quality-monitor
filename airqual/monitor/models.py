from django.db import models
from django.utils import timezone
# Create your models here.

class DataPoint(models.Model):
    value = models.IntegerField(default = 0)
    timestamp = models.DateTimeField('date added')

#class Sensor(models.Model):
    #owner
    #values
    #name

