from rest_framework import serializers
from .models import Car, Rate

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','make','model','avg_rating']


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate','car_id']


class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','make','model','rates_number']