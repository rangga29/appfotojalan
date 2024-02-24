from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.fields import SerializerMethodField
from titiksurvei.models import survei
from django.templatetags.static import static
from django.conf import settings

class surveiSerializer(GeoFeatureModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = survei
        fields = ("id_survei", "survey_name", "frame_filename", "latitude", "longitude", "image_url")
        geo_field = "mpoint"

    def get_image_url(self, obj):
        if obj.frame_filename:
            # If you have the image in the static directory
            return static('images/' + obj.frame_filename)
            # If you are using media files, you should use:
            # return obj.image.url if obj.image else None
        return None
