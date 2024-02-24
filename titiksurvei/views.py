from django.shortcuts import render, Http404
from .models import survei
from .serializers import surveiSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.templatetags.static import static
from django.conf import settings
#from .utils import apply_projective_transformation_with_gdal  # Import the function you created
from osgeo import gdal, osr
from PIL import Image
import os
import cv2
import numpy as np
import io
import logging
import time

# Enable GDAL/OGR exceptions
gdal.UseExceptions()

# Create your views here.
from django.views.generic.base import (
    TemplateView,
)


class MarkersMapView(TemplateView):
    template_name = 'map.html'

def get_context_data(self, **kwargs):
        context = super(MarkersMapView, self).get_context_data(**kwargs)
        survei_qs = survei.objects.all()
        # Pass the request to the serializer to get full image URLs
        context['survei_data'] = surveiSerializer(survei_qs, many=True, context={'request': self.request}).data
        return context

def display_image(request, image_name):
    # Assuming the images are in a folder named 'display_image' inside your static directory
    image_url = static('images/' + image_name)
    return render(request, 'image_display.html', {'image_url': image_url})

#IMAGE PROCESSING AND RATING

# Initialize global variables
click_points = []  # List to store click points
measurement_active = False  # Flag to indicate if we're currently measuring
zoom_level = 100  # Initial zoom level in percentage (100% means no zoom)

# Function to resize the image based on the zoom level
def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

# Updated function to display the rectified image with grid and handle zoom
def update_display_image():
    global rectified_image_with_grid, zoom_level
    resized_image = resize_image(rectified_image_with_grid, zoom_level)
    cv2.imshow('Rectified Image with Grid', resized_image)

def overlay_grid(image, grid_size):
    """Overlay a grid on the rectified image with a floating-point grid size, starting from the bottom."""
    height, width = image.shape[:2]

    # Vertical lines
    x = 0.0
    while x < width:
        cv2.line(image, (int(round(x)), 0), (int(round(x)), height), (255, 255, 255), 1)
        x += grid_size  # Move to the next position by grid_size

    # Horizontal lines, starting from the bottom
    y = height
    while y > 0:
        cv2.line(image, (0, int(round(y))), (width, int(round(y))), (255, 255, 255), 1)
        y -= grid_size  # Move to the next position by grid_size, going upwards

    return image

def rectify_image(image, src_points, dst_points):
    """Apply perspective transformation to rectify the image."""
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    # Determine the bounds for the entire image after transformation
    height, width = image.shape[:2]
    result = cv2.warpPerspective(image, matrix, (width, height))  # Use original image dimensions
    return result


def measure_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def click_event(event, x, y, flags, param):
    global click_points, measurement_active, rectified_image_with_grid, zoom_level

    if event == cv2.EVENT_LBUTTONDOWN and measurement_active:
        click_points.append((x, y))
        cv2.circle(rectified_image_with_grid, (x, y), 5, (0, 0, 255), -1)

        if len(click_points) == 2:
            distance = measure_distance(click_points[0], click_points[1])
            scale_factor = 0.017761877  # Adjust the scale factor as per your requirements
            distance_in_meters = distance * scale_factor
            measurement_text = f"{distance_in_meters:.2f} meters"  # Text to display

            # Draw the line between the points
            cv2.line(rectified_image_with_grid, click_points[0], click_points[1], (0, 255, 0), 2)

            # Calculate the midpoint for the text position
            text_position = (int((click_points[0][0] + click_points[1][0]) / 2), int((click_points[0][1] + click_points[1][1]) / 2))

            # Draw the text on the image
            cv2.putText(rectified_image_with_grid, measurement_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, (0, 0, 0), 2)

            click_points = []  # Reset for next measurement
            measurement_active = False  # Optionally, stop measurement mode
            
            # Update the display to show the measurement line and text
            update_display_image()

    elif event == cv2.EVENT_RBUTTONDOWN and measurement_active:
        # Reset the measurement process
        click_points = []
        measurement_active = False
        # You may want to clear any existing drawings from previous measurements here
        rectified_image_with_grid = overlay_grid(rectify_image(image, src_points, dst_points).copy(), grid_size)
        update_display_image()

    # Handle zooming with the mouse wheel as before
    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:  # Scroll up to zoom in
            zoom_level = min(zoom_level + 10, 400)  # Limit maximum zoom to 400%
        else:  # Scroll down to zoom out
            zoom_level = max(zoom_level - 10, 10)  # Limit minimum zoom to 10%
        update_display_image()

# Load and process the image
image = cv2.imread('C:/Users/Jesika Taradini/appfotojalan/titiksurvei/static/images/KAMERAROMDAS2-ROW-0-00001_dimensi.jpg')
src_points = np.float32([
    [154.80107474120484, 757.1474897915689], # Bottom-left
    [874.3604806817992, 757.661216164206], # Bottom-right
    [634.7927489086217, 482.2182593685262], # Top-right
    [411.0649136250936, 482.2610698995794] # Top-left
])

dst_points = np.float32([
    [154.80107474120484, 757.1474897915689], # Bottom-left
    [377.6010747, 757.661216164206], # Bottom-right
    [377.6010747, 200], # Top-right
    [154.80107474120484, 200] # Top-left
])

start_time = time.time()
rectified_image = rectify_image(image, src_points, dst_points)
grid_size = 56.30035524
rectified_image_with_grid = overlay_grid(rectified_image.copy(), grid_size)
end_time = time.time()
duration = end_time - start_time

# Initial display of the rectified image with grid
update_display_image()

# Set up the window and callback
cv2.namedWindow('Rectified Image with Grid')
cv2.setMouseCallback('Rectified Image with Grid', click_event)

# Display the image and wait for user interaction
measurement_active = True
cv2.imshow('Rectified Image with Grid', rectified_image_with_grid)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Time taken for perspective transformation and display: {duration} seconds")