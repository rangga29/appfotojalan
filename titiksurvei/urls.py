from django.urls import path
from titiksurvei.views import MarkersMapView
from . import views

# Import settings and static utility function for serving media files
from django.conf import settings
from django.conf.urls.static import static

app_name = 'titiksurvei'

urlpatterns = [
    path('map/', MarkersMapView.as_view()),
    path('display_image/<str:image_name>/', views.display_image, name='display_image'),
    #path('transform-image/', gdal_proj_transformation, name='transform-image'),
    #path('georeferenced-image/', views.show_georeferenced_image, name='georeferenced-image'),
]

# During development, use Django to serve media files uploaded by users
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
