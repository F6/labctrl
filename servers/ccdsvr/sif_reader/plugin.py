import numpy as np
from collections import OrderedDict
from PIL import Image, ImageFile
from . import _sif_open

# Read Andor Technology Multi-Channel files with PIL.
# Based on Marcel Leutenegger's MATLAB script.

class SifImageFile(ImageFile.ImageFile):
    format = "SIF"
    format_description = "Andor Technology Multi-Channel File"

    def _open(self):
        title, size, no_images, info = _sif_open._open(self.fp)
        self.title = title
        self.size[:] = size[:]
        # self.size = size
        for key, item in info.items():
            self.info[key] = item

        self.mode = 'F'

        #self.fp.seek(tile[2])  # offset

# Registry
Image.register_open("SIF", SifImageFile)
Image.register_extension("SIF", ".sif")
