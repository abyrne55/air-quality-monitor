from django.db import models

# Create your models here.

class DataPoint(models.Model):
    value = models.IntegerField(default = 0)

class Sensor(models.Model):
    #owner
    #values
    #name

