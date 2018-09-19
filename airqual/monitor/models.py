import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class DataPoint(models.Model):
    # Value of the data being reported
    value = models.DecimalField(max_digits=6, decimal_places=2)

    # Immutable timestamp
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

class Sensor(models.Model):
    # Friendly name of the sensor (shown in UI)
    name = models.CharField(max_length=100)

    # User that 'owns' this sensor
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # API key for the sensor, allowing data to be sent to the API
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)

    # All DataPoints related to this sensor
    data = models.ManyToManyField(DataPoint, blank=True)

    # Unit of data collected by this sensor (shown in UI)
    unit = models.CharField(max_length=10, default="°C")

    # Sanity checks: posted values must be inside this range to avoid triggering a warning
    min_value = models.DecimalField(max_digits=6, decimal_places=2)
    max_value = models.DecimalField(max_digits=6, decimal_places=2)
    malfunction = models.BooleanField(default=False) # toggled if value posted out of bounds

    def __str__(self):
        return self.name
