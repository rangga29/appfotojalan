from django.shortcuts import render

# Create your views here.
# world/views.py

from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from .models import WorldBorder

def get_geojson(request):
    data = WorldBorder.objects.all()
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for point in data:
        feature = {
            "type": "Feature",
            "geometry": GEOSGeometry(point.mpoly).json,
            "properties": {
                "name": point.name
            }
        }
        geojson_data["features"].append(feature)

    return JsonResponse(geojson_data, safe=False)
