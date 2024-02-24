from django.contrib import admin
from django.contrib.gis import admin
from titiksurvei.models import Marker
from titiksurvei.models import survei

# Register your models here.
@admin.register(Marker)
class MarkerAdmin(admin.GISModelAdmin):
    list_display = ("name", "location")

@admin.register(survei)
class surveiAdmin(admin.GISModelAdmin):
    list_display = ("id_survei", "survey_name", "frame_filename", "latitude", "longitude")