
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import CarSerializer, RateSerializer, PopularSerializer
from .models import Car, Rate
import json
# Create your views here.


def car_check(model,make):
    add_car = False
    model = model.upper()
    url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{model}?format=json'
    car_request = requests.get(url)
    data = json.loads(car_request.text)['Results']
    for car_record in data:
        if make.lower() == car_record['Model_Name'].lower():
            add_car = True
    return add_car


def avr_car(car_id):
    rats = Rate.objects.filter(car_id=car_id).values()
    total_ratings = 0
    i = 0
    for ocena in rats:
        total_ratings += (ocena['rate'])
        i += 1
    return round(total_ratings / i, 2)


@api_view(['GET','POST'])
def cars(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        serializer = CarSerializer(cars,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        make = data["make"]
        model = data["model"].lower()
        serielizer = CarSerializer(data=data)
        if serielizer.is_valid():
            if car_check(make, model) and not Car.objects.filter(make=make).filter(model=model).exists():
                serielizer.save()
                return Response(serielizer.data,status=status.HTTP_201_CREATED)
        return Response(serielizer.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cars_delete(request,pk):
    try:
        car = Car.objects.get(pk=pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def rate(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pk = data["car_id"]
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        avr_rate = avr_car(pk)

        serielizer = RateSerializer(data = data)

        if serielizer.is_valid():
            serielizer.save()
            car.rates_number += 1
            car.avg_rating = avr_rate
            car.save(update_fields=['rates_number','avg_rating'])
            return Response(serielizer.data,status=status.HTTP_201_CREATED)
        return Response(serielizer.errors, status= status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def popular(request):
    if request.method == 'GET':
        cars = Car.objects.order_by('-rates_number')
        serializer = PopularSerializer(cars,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)