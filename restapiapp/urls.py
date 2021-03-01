from django.urls import path
from .views import cars, cars_delete, rate, popular

urlpatterns = [
    path('cars/', cars),
    path('cars/<int:pk>/', cars_delete),
    path('rate/', rate),
    path('popular/',popular)
    ]