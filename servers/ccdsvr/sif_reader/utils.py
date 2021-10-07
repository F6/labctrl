import numpy as np


def extract_calibration(info):
    """
    Extract calibration data from info.

    Parameters
    ----------
    info: OrderedDict
        OrderedDict from np_open

    Returns
    -------
    calibration:
        np.ndarray.
        1d array sized [width] if only 1 calibration is found.
        2d array sized [NumberOfFrames x width] if multiple calibration is
            found.
        None if no calibration is found
    """
    width = info['DetectorDimensions'][0]
    # multiple calibration data is stored
    if 'Calibration_data_for_frame_1' in info:
        calibration = np.ndarray((info['NumberOfFrames'], width))
        for f in range(len(calibration)):
            key = 'Calibration_data_for_frame_{:d}'.format(f + 1)
            flip_coef = np.flipud(info[key])
            calibration[f] = np.poly1d(flip_coef)(np.arange(1, width + 1))
        return calibration

    elif 'Calibration_data' in info:
        flip_coef = np.flipud(info['Calibration_data'])
        return np.poly1d(flip_coef)(np.arange(1, width + 1))
    else:
        return None
