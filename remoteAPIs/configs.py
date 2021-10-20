# -*- coding: utf-8 -*-

"""configs.py:
Basic configurations for remote APIs.
    - IP addresses and ports
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


# region Configs

# CCD_ip = '192.168.1.243'
# ir_stage_ip = '192.168.1.243'
# ir_topas_serial_number = "17627"
# vis_topas_serial_number = "17623"
# shutter_ip = '127.0.0.1'
# PD_ip = '127.0.0.1'
# CCD_base_address = "http://{}:5000/".format(CCD_ip)
# ir_stage_base_address = "http://{}:5001/".format(ir_stage_ip)
# shutter_base_address = "http://{}:5000/".format(shutter_ip)
# PD_base_address = "http://{}:5003/".format(PD_ip)

# for dev tests
CCD_ip = '127.0.0.1'
ir_stage_ip = '127.0.0.1'
ir_topas_serial_number = "00000"
vis_topas_serial_number = "00001"
shutter_ip = '127.0.0.1'
PD_ip = '127.0.0.1'
monochromer_ip = '127.0.0.1'
toupcam_ip = '127.0.0.1'

CCD_base_address = "http://{}:5000/".format(CCD_ip)
ir_stage_base_address = "http://{}:5001/".format(ir_stage_ip)
shutter_base_address = "http://{}:5002/".format(shutter_ip)
PD_base_address = "http://{}:5003/".format(PD_ip)
monochromer_base_address = "http://{}:5004/".format(monochromer_ip)
toupcam_base_address = "http://{}:5005/".format(toupcam_ip)


ports = {
    "EMCCD": 5000,  # Electron multiplying CCD at Andor SOLIS
    "CDHD2": 5001,  # The flat linear stage for IR topas delay line
    "Shutter": 5002,  # Shutter controller
    "RigolOscilloscope": 5003,  # Rigol oscilloscope (the black one)
    "Monochromer": 5004,  # The black one at A304
    "ToupCam": 5005,  # ToupTek USB Cameras
    # 5006 is taken by bokeh server
    "USB1020": 5007,  # Motion controller, the short one now for pumpprobe
    "PMC48MT6": 5008,  # Motion controller, the 3500ps one for visible topas
}


# endregion
