from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import survei

survei_mapping ={
    "id": "fid",
    "id_survei": "id",
    "survey_name": "survey_nam",
    "frame_filename": "frame_file",
    "latitude": "latitude",
    "longitude": "longitude",
    "mpoint": "multipoint",
}

survei_shp = Path(__file__).resolve().parent/"data"/"36052_R1.shp"

def run(verbose=True):
    lm = LayerMapping(survei, survei_shp, survei_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)