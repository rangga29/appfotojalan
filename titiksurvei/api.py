from rest_framework import routers

from titiksurvei.viewsets import (
    surveiViewSet,
)

router = routers.DefaultRouter()
router.register(
    r"survei", surveiViewSet
)

urlpatterns = router.urls