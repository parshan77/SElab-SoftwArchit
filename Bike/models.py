from django.db import models


class Bike(models.Model):
    unique_id = models.PositiveIntegerField(unique=True)
    available = models.BooleanField(default=True)
    locationX = models.IntegerField(blank=True, null=True)
    locationY = models.IntegerField(blank=True, null=True)
    
    
    
