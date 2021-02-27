from django.db import models

# Create your models here.
class Car (models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    rates_number = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.make
