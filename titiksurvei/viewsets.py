from rest_framework import viewsets
from rest_framework_gis import filters

from titiksurvei.models import survei
from titiksurvei.serializers import (
    surveiSerializer,
)


class surveiViewSet(
    viewsets.ReadOnlyModelViewSet
):
    bbox_filter_field = "mpoint"
    filter_backends = (
        filters.InBBoxFilter,
    )
    queryset = survei.objects.all()
    serializer_class = surveiSerializer