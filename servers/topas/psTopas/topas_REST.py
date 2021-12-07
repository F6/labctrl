# -*- coding: utf-8 -*-

"""topas_REST.py:
This module provides class Topas4Controller to control TOPAS in our lab.
A Topas4Emulator class is also provided for dev emulation without
actually send commands to TOPAS

To set wavelength, the host computer that runs this program needs to be
authorized from the TOPAS server. To do this, open the official TOPAS
client app and select server - authorize another computer - input the IP
address of this computer - click start authorization - press interactive
lock button on the physical TOPAS device repeatedly
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"


import requests
import sys
import msvcrt
from .Topas4Locator import Topas4Locator


class Topas4Controller:
    baseAddress = None
    interactions = None

    def __init__(self, serialNumber):
        locator = Topas4Locator()
        availableDevices = locator.locate()
        match = next(
            (obj for obj in availableDevices if obj['SerialNumber'] == serialNumber), None)
        if match is None:
            print('Device with serial number %s not found' % serialNumber)
        else:
            self.baseAddress = match['PublicApiRestUrl_Version0']

    def put(self, url, data):
        return requests.put(self.baseAddress + url, json=data)

    def post(self, url, data):
        return requests.post(self.baseAddress + url, json=data)

    def get(self, url):
        return requests.get(self.baseAddress + url)

    def getCalibrationInfo(self):
        self.interactions = self.get(
            '/Optical/WavelengthControl/ExpandedInteractions').json()
        print("Available interactions:")
        for item in self.interactions:
            print(item['Type'] + " %d - %d nm" %
                  (item['OutputRange']['From'], item['OutputRange']['To']))
        if len(self.interactions) == 0:
            print("Warning: There is no calibrated interaction available!")

    def setWavelength(self, interaction, wavelength_to_set):
        print("Setting wavelength %.4f nm using interaction %s" %
              (wavelength_to_set, interaction['Type']))
        if wavelength_to_set < interaction['OutputRange']['From'] or wavelength_to_set > interaction['OutputRange']['To']:
            print("Sanity Check: Wavelength out of range! Cannot set wavelength to {wts} with interaction {it} ({wf} - {wt} nm)".format(
                wls=wavelength_to_set, it=interaction['Type'], wf=interaction['OutputRange']['From'], wt=interaction['OutputRange']['To']))
        response = self.put('/Optical/WavelengthControl/SetWavelength',
                            {'Interaction': interaction['Type'], 'Wavelength': wavelength_to_set})
        print("Wavelength setting begins, topas remote says", response)
        # if I don't care about interaction used:
        #response =self.put('/Optical/WavelengthControl/SetWavelengthUsingAnyInteraction',wavelength_to_set)
        self.waitTillWavelengthIsSet()

    def checkShutterStatus(self):
        isShutterOpen = self.get('/ShutterInterlock/IsShutterOpen').json()
        return isShutterOpen

    def changeShutter(self):
        isShutterOpen = self.get('/ShutterInterlock/IsShutterOpen').json()
        line = input(r"Do you want to " +
                     ("close" if isShutterOpen else "open") + r" shutter? (Y\N)").upper()
        if line == "Y" or line == "YES":
            self.put('/ShutterInterlock/OpenCloseShutter', not isShutterOpen)

    def waitTillWavelengthIsSet(self):
        """
        Waits till wavelength setting is finished.  If user needs to do any manual
        operations (e.g.  change wavelength separator), inform him/her and wait for confirmation.
        """
        while(True):
            s = self.get('/Optical/WavelengthControl/Output').json()
            sys.stdout.write("\r %d %% done" %
                             (s['WavelengthSettingCompletionPart'] * 100.0))
            if s['IsWavelengthSettingInProgress'] == False or s['IsWaitingForUserAction']:
                break
        state = self.get('/Optical/WavelengthControl/Output').json()
        if state['IsWaitingForUserAction']:
            print("\nUser actions required. Press enter key to confirm.")
            # inform user what needs to be done
            for item in state['Messages']:
                print(item['Text'] + ' ' + ('' if item['Image']
                      is None else ', image name: ' + item['Image']))
            sys.stdin.read(1)  # wait for user confirmation
            # tell the device that required actions have been performed.  If shutter was open before setting wavelength it will be opened again
            self.put('/Optical/WavelengthControl/FinishWavelengthSettingAfterUserActions',
                     {'RestoreShutter': True})
        print("Done setting wavelength")

    def tweakMotorPositions(self, motor):
        """move single motor to desired position and read current position"""
        print(r"Press Up/Down arrow keys to move motor " +
              motor['Title'] + ". Press Escape to finish motor position tweaking.")
        motorIndex = motor['Index']
        while (True):
            key = ord(msvcrt.getch())
            if key == 27:  # ESC
                return
            elif key == 224:  # Special keys
                key = ord(msvcrt.getch())
                if key == 72:  # Up arrow
                    current = self.get(
                        '/Motors/TargetPosition?id=%i' % motorIndex).json()
                    self.put('/Motors/TargetPosition?id=%i' %
                             motorIndex, current + 8)
                    # steps, if you want to use units use TargetPositionInUnits
                elif key == 80:  # Down arrow
                    self.put('/Motors/TargetPositionRelative?id=%i' %
                             motorIndex, -8)
                    # equivalent functionality to UpArrow
                else:
                    print(
                        "Invalid key. Use Escape to stop motor position adjustment, Up and Down arrows to move motor.")
            else:
                print(
                    "Invalid key. Use Escape to stop motor position adjustment, Up and Down arrows to move motor.")


class Topas4Emulator:
    baseAddress = None
    interactions = None

    def __init__(self, serialNumber):
        pass

    def getCalibrationInfo(self):
        self.interactions = [
            {'Type': 'EmulatorInteraction{}'.format(i)} for i in range(20)]
        for item in self.interactions:
            print(item)
        if len(self.interactions) == 0:
            print("Warning: There is no calibrated interaction available!")

    def setWavelength(self, interaction, wavelength_to_set):
        print("Setting wavelength %.4f nm using interaction %s" %
              (wavelength_to_set, interaction))
        print("Wavelength setting begins, topas remote says", "[EmulatorOK]")

        self.waitTillWavelengthIsSet()

    def checkShutterStatus(self):

        return True

    def waitTillWavelengthIsSet(self):

        print("[Emulator] Done setting wavelength")
