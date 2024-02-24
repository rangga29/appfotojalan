from django.conf import settings
import os
from PIL import Image, ImageDraw

# Load an image
# Define the relative path to the image within the static directory
image_relative_path = 'images/36052_R1-ROW-0-00001.jpg'  # Adjust the path

# Combine with the base directory
image_path = os.path.join(settings.BASE_DIR, 'static', image_relative_path)

# Now, you can load and process the image
image = Image.open(image_path)

# Draw a simple grid
draw = ImageDraw.Draw(image)
spacing = 50  # Adjust as needed
for x in range(0, image.width, spacing):
    draw.line((x, 0, x, image.height), fill=128)
for y in range(0, image.height, spacing):
    draw.line((0, y, image.width, y), fill=128)

image.show()  # Display the image with the grid

# Save the image with the grid
processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_images', 'my_image_with_grid.jpg')
image.save(processed_image_path)