# urls.py
from django.urls import path
from .views import get_geojson

urlpatterns = [
    path('map/', get_geojson, name='map'),
]
