from django.db import models

# Create your models here.
from django.contrib.gis.db import models

class Marker(models.Model):
    name = models.CharField(
        max_length=255
    )
    location = models.PointField()

class survei(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_survei = models.IntegerField()
    survey_name = models.CharField()
    frame_filename = models.CharField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    mpoint = models.MultiPointField(srid=4326)
    

    def __int__(self):
        return self.id_survei