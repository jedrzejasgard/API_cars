from rest_framework import serializers
from .models import Car

class CerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['make','model','avg_rating','rates_number']