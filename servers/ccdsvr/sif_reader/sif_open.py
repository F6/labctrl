import numpy as np
from collections import OrderedDict
from ._sif_open import _open
from .utils import extract_calibration

def np_open(sif_file):
    """
    Open sif_file and return as np.array.
    """
    try:
        f = sif_file
        tile, size, no_images, info = _open(f)
    except AttributeError:
        f = open(sif_file,'rb')
        tile, size, no_images, info = _open(f)
    # allocate np.array
    data = np.ndarray((no_images, size[1], size[0]), dtype=np.float32)
    for i, tile1 in enumerate(tile):
        f.seek(tile1[2])  # offset
        data[i] = np.fromfile(f, count=size[0]*size[1],dtype='<f').reshape(size[1],size[0])

    try:
        f.close()
    finally:
        pass

    return data, info

# --- xarray open ---
try:
    import xarray as xr

    def xr_open(sif_file):
        """
        Read file and set into xr.DataArray.
        """
        data, info = np_open(sif_file)
        # coordinates
        coords = OrderedDict()
        # extract time stamps
        time = np.ndarray(len(data), dtype=np.float)
        for f in range(len(data)):
            time[f] = info['timestamp_of_{0:d}'.format(f)] * 1.0e-6  # unit [s]
            del info['timestamp_of_{0:d}'.format(f)]
        coords['Time'] = (('Time', ), time, {'Unit': 's'})

        # calibration data
        x_calibration = extract_calibration(info)
        if x_calibration is not None:
            if x_calibration.ndim == 2 and x_calibration.shape == (data.shape[0], data.shape[2]):
                coords['calibration'] = (('Time', 'width'), x_calibration)
            elif x_calibration.shape == x_calibration.shape == (data.shape[2], ):
                coords['calibration'] = (('width'), x_calibration)

        new_info = OrderedDict()
        for key in info:
            if 'Calibration_data' not in key:
                new_info[key] = info[key]

        return xr.DataArray(data, dims=['Time', 'height', 'width'],
                            coords=coords, attrs=new_info)


except ImportError:
    pass
