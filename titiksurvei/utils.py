import cv2
import numpy as np
import logging
from osgeo import gdal, osr

import cv2
import numpy as np
import logging

# Enable GDAL/OGR exceptions
gdal.UseExceptions()

# Get an instance of a logger
logger = logging.getLogger(__name__)