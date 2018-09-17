from django.db import models
from django.utils import timezone
# Create your models here.

class DataPoint(models.Model):
    value = models.IntegerField(default = 0)
    timestamp = models.DateTimeField('date added')

class Sensor(models.Model):
    owner = models.CharField(max_length=200, default='no owner')
    sensor_id = models.CharField(max_length=200, default = 'default')
    data = models.ManyToManyField(DataPoint)
    def __str__(self):
        return self.sensor_id
