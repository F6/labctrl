# -*- coding: utf-8 -*-

"""Topas4Locator.py:
This module provides class Topas4Locator to find local
Topas4 devices. The module is modified from TOPAS official
SDK, please check their website for licensing and copyright
information
"""

__author__ = "Light Conversion, UAB"
__email__ = "support@lightcon.com"
__version__ = "20211003"


import socket
import json


class Topas4Locator:
    """"Locates Topas4 devices on the same local area network using UDP multicast"""

    def locate(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        multicastAddress = ('239.0.0.181', 7415)
        # works as loopback broadcast for reused sockets
        localHostAddress = ('127.255.255.255', 7415)
        message = 'Topas4?'.encode('UTF-8')
        devices = []

        # Send data both to multicast address and to localhost
        # localhost is for cases when server and client applications are running on the same PC, and PC might be not connected to the network
        sock.sendto(message, multicastAddress)
        sock.sendto(message, localHostAddress)

        while (True):
            sock.settimeout(1.0)
            sock
            try:
                data, sender = sock.recvfrom(4096)
            except socket.timeout:
                break

            try:
                description = json.loads(data.decode('UTF8'))
                if description['Identifier'] == 'Topas4':
                    devices.append(description)
            except json.decoder.JSONDecodeError:
                print('bad data received by locator')

        sock.close()
        uDev = []
        seen = set()
        # multiple answers from the same device are possible, and certain if server is located on the same PC
        uniqDevices = [obj for obj in devices if obj['SenderGUID']
                       not in seen and not seen.add(obj['SenderGUID'])]

        return uniqDevices
