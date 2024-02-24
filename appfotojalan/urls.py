from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('titiksurvei.api')),
    path('titiksurvei/', include('titiksurvei.urls')),
    # Uncomment or add other paths as needed
    # path('appfotojalan/', include('appfotojalan.urls')),
    # path('', include('world.urls')),
]

# This part serves static files like CSS, JavaScript, and images in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add this line to serve media files uploaded by users during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
