# -*- coding: utf-8 -*-
"""
@author: Jörg Encke, Wilfried Hortschitz, Matthias Kahr, Veronika Schrenk
This class is able to connect to the Stanford Lock-In Amplifier SR830, 
regardless what Gpib-Adress the Amplifier is set.
All major functionalities have been implemented in public methods.
Literature - References:
[1]
MODEL SR830 DSP Lock-In Amplifier - Manual
by Stanford Research Systems
Revision 2.5 (10/2011)
http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
"""
import time
import imp
import sys
import warnings
import subprocess
import numpy as np

DEBUG = False
DEVICE_NAME = "Stanford_Research_Systems,SR830"


class liaSR830():

    def __lin_search_logic(self):
        """
        This function is meant to be called from __init__ to automatically search
        for the correct gpib-address in ubuntu
        """
        try:
            f, filename, descr = imp.find_module('Gpib')
            Gpib_package = imp.load_module('Gpib', f, filename, descr)
            f, filename, descr = imp.find_module('gpib')
            gpib_package = imp.load_module('gpib', f, filename, descr)
            gpib_available = True
        except ImportError:
            gpib_available = False
            print('Gpib is not available')
        if gpib_available:
            print("searching for correct gpib-address...")
            for x in range(1, 31):
                try:
                    self.inst = Gpib_package.Gpib(0, x)
                    self.inst.clear()
                    self.inst.write('*idn?')
                    time.sleep(0.8)
                    print(
                        "Stanford_Research_System, SR830 on gpib-address " + str(x) + " detected!")
                    return True
                    break
                except gpib_package.GpibError as e:
                    print(str(x) + " ...")
                    continue
        return False

    def __check_if_GPIB_USB_B_Adapter_linux(self):
        """
        internal method
        this method checks if the GPIB-USB-B-Adapter is used instead of the GPIB-USB-HS-Adapter.
        if this condition is true the method loads all needed modules in Ubuntu      
        """
        a = []
        a = subprocess.check_output('lsusb')
        x = None
        for i in a.split('\n'):
            if 'GPIB-USB-B' in i:
                x = i
                break
        if x is not None:
            bus_number = x[4:7]
            device_number = x[15:18]
            subprocess.Popen('sudo fxload -D /dev/bus/usb/' + str(bus_number) + '/' + str(device_number) +
                             ' -I /lib/firmware/ni_usb_gpib/niusbb_firmware.hex -s /lib/firmware/ni_usb_gpib/niusbb_loader.hex',
                             shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def __init__(self):
        '''
        Automatically search for pre-set gpib-address from connected instrument
        Check if the connected Intrument is compatible to this driver by
        using check_instr-function        
        '''
        found = False

        if sys.platform.startswith('lin'):
            self.__check_if_GPIB_USB_B_Adapter_linux()
            found = self.__lin_search_logic()
            if not found:
                #print("Run \'sudo gpib_config\'")
                subprocess.Popen('sudo gpib_config', shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                print("Gpib-address could not be detected!")
                print("Press F5...")

        elif sys.platform.startswith('win'):
            try:
                f, filename, descr = imp.find_module('visa')
                visa_package = imp.load_module('visa', f, filename, descr)
                visa_available = True
            except ImportError:
                visa_available = False
                print('Visa is not available')
            if visa_available:
                rm = visa_package.ResourceManager()

                print("searching for correct gpib-address...")
                for x in range(1, 31):
                    with warnings.catch_warnings(record=True) as w:
                        self.visa_instr = rm.open_resource(
                            'GPIB0::' + str(x) + '::INSTR')
                    if len(w):
                        print(str(x) + " ...")
                        continue
                    else:
                        print(str(x) + " ...")
                        if(self.check_instr()):
                            print(
                                "Stanford_Research_System, SR830 on gpib-address " + str(x) + " detected!")
                            found = True
                            break
                if not found:
                    print("Gpib-address could not be detected!")

    def check_instr(self):
        '''
        Check if the connected Intrument is compatible to this driver by
        comparing the *IDN? answer to the string "Stanford_Research_Systems,SR830"        
        '''
        if sys.platform.startswith('lin'):
            self.inst.clear()
            self.inst.write('*idn?')
            time.sleep(0.2)
            ident = self.inst.read(100)
            self.inst.clear()
        elif sys.platform.startswith('win'):
            self.visa_instr.clear()
            try:
                ident = self.visa_instr.query("*IDN?")
                time.sleep(3)
            except:
                ident = ""
            self.visa_instr.clear()
        if DEVICE_NAME in ident:
            return True
        else:
            if DEBUG:
                print("DEBUG: Instrument " + ident +
                      " seems not to be Stanford_Research_Systems, SR830")
            return False

    def correct_phaseshift(self, phase):
        """
        I have no idea what this method is supposed to do (-> untested)
        """
        th = 100
        def sig(x): return x < 0.

        prev_sig = sig(phase[0])
        prev_element = phase[0]
        jump = 0
        return_array = []

        for element in phase:
            save_element = element
            if (sig(element) is not prev_sig
                and abs(prev_element) > th
                    and abs(element) > th):

                if jump:
                    jump = 0

                else:
                    jump = -1 if prev_sig else 1

            if jump:
                save_element = element + jump * 360

            prev_element = element
            prev_sig = sig(element)
            return_array.append(save_element)
            return return_array

    def __GetSomething(self, cmdString):
        """
        Internal function. The cmdString will be send to the instrument
        to get a response. 
        (cmdString can be for example SENS?, FREQ?,... most likely something with a question mark)
        """
        if sys.platform.startswith('win'):
            self.visa_instr.clear()
            resp = self.visa_instr.query(cmdString)
        elif sys.platform.startswith('lin'):
            self.inst.clear()
            self.inst.write(cmdString)
            resp = self.inst.read(100)
            self.inst.clear()
        if DEBUG:
            print("command: " + cmdString + "; resp: " + str(resp))
        return resp

    def __SetSomething(self, cmdString, setValue):
        """
        Internal function. The cmdString will be send to the instrument. 
        Use setValue to set specific Values on the instrument 
        (setValue can for example be the value of PHAS or FREQ, 
        when the cmdString contains "PHAS" or "FREQ")
        """
        if sys.platform.startswith('win'):
            self.visa_instr.write(cmdString + ' ' + str(setValue))
        elif sys.platform.startswith('lin'):
            self.inst.clear()
            self.inst.write(cmdString + ' ' + str(setValue))
            time.sleep(0.2)
            self.inst.clear()
        if DEBUG:
            print("command: " + cmdString + ' ' + str(setValue))

    def ConvertiToTimeconstant(self, i):
        """
        converts the i-param needed for the OFLT?-command to the actual timeconstant-value
        """
        options = {0: 10e-6,
                   1: 30e-6,
                   2: 100e-6,
                   3: 300e-6,
                   4: 1e-3,
                   5: 3e-3,
                   6: 10e-3,
                   7: 30e-3,
                   8: 100e-3,
                   9: 300e-3,
                   10: 1,
                   11: 3,
                   12: 10,
                   13: 30,
                   14: 100,
                   15: 300,
                   16: 1000,
                   17: 3000,
                   18: 10000,
                   19: 30000
                   }
        try:
            return options[i]
        except:
            raise Exception(
                "ConvertiToTimeconstant: parameter i contains an invalid value")

    def ConvertTimeconstantToi(self, timeconstant):
        """
        converts the actual timeconstant-value to the i-param, needed for the OFLT-command
        """
        options = {10e-6: 0,
                   30e-6: 1,
                   100e-6: 2,
                   300e-6: 3,
                   1e-3: 4,
                   3e-3: 5,
                   10e-3: 6,
                   30e-3: 7,
                   100e-3: 8,
                   300e-3: 9,
                   1: 10,
                   3: 11,
                   10: 12,
                   30: 13,
                   100: 14,
                   300: 15,
                   1000: 16,
                   3000: 17,
                   10000: 18,
                   30000: 19
                   }
        try:
            return options[timeconstant]
        except:
            raise Exception(
                "ConvertTimeconstantToi: parameter timeconstant contains an invalid value")

# by HoWil#############

    def __SensitivityToVolt(self, n_In):
        """
        Internal method
        This function is meant to be called from .SetSensitivityLIA() to calculate 
        the sensitivity value out of the sensitivity settings on the lockIn
        """
        # Dim m_In As Integer
        m_In = n_In + 1
        voltValue = round(10**((m_In % 3) / 3)) * \
            (10**-9 * 10**np.floor(m_In / 3))
        return voltValue
    # end % function SensitivityToVolt

    def SetSensitivityLIA(self, timeconstant=None):
        """
        Automatically sets the best Sensitivity.

        When the timeconstant is None the timeconstant set on the device
        is being used. Attention: If this pre-set timeconstant is large, this could take awhile!
        When the timecontant is not None, the timeconstant on the device is set to this timeconstant,
        before the SetSensitivityLIA-Logic starts         
        """
        # Configure property value(s).
        #set(obj, 'sens', 22.0);

        bKorrekterBereich = 0
        Frequenz = self.getF()
        T = 1/Frequenz

        while bKorrekterBereich == 0:
            if timeconstant == None:
                i = self.GetTimeConst()
                timeconstant = self.ConvertiToTimeconstant(i)
                time.sleep(3 * timeconstant + T)
            else:
                i = self.ConvertTimeconstantToi(timeconstant)
                self.SetTimeConst(i)
                time.sleep(3 * timeconstant + T)
            # end

            # Query property value(s).
            iSensitivityLIA = self.getSens()  # get the set sensitivity
            R = self.getR()
            # print " R = %f" %R
            # print " iSensitivityLIA = %i" %iSensitivityLIA
            vValue = self.__SensitivityToVolt(iSensitivityLIA)  # !!!
            # print " voltValue = %f" %voltValue
            if R > vValue:
                iSensitivityLIA = iSensitivityLIA + 1
                if iSensitivityLIA > 26:
                    iSensitivityLIA = 26
                # end;
                # Configure property value(s).
                self.SetSens(iSensitivityLIA)
                bKorrekterBereich = 0
                time.sleep(3 * timeconstant + 0.2 * T)
            else:
                #R = self.getR();
                # vValue = self.__SensitivityToVolt(iSensitivityLIA);#!!!
                if DEBUG:
                    print(str(vValue))

                if R < 0.3 * vValue:
                    iSensitivityLIA = iSensitivityLIA - 1
                    if iSensitivityLIA < 0:
                        iSensitivityLIA = 0
                    # end;
                    if DEBUG:
                        print("iSensitivityLIA: " + str(iSensitivityLIA))
                    self.SetSens(iSensitivityLIA)
                    bKorrekterBereich = 0
                    time.sleep(3 * timeconstant + 0.2 * T)
                else:
                    bKorrekterBereich = 1

        if DEBUG:
            print(str(vValue))
        return vValue
        # end
        # end
        # end

    # end # function SetSensitivityLIA

    def SendString(self, CmdString):
        """
        sends CmdString as a command to the instrument
        """
        if DEBUG:
            print("send string: " + CmdString)

        if sys.platform.startswith('win'):
            self.visa_instr.write(CmdString)
        elif sys.platform.startswith('lin'):
            self.inst.write(CmdString)
        return

    def getR(self):
        """
        Query the value of R (3). Returns ASCII floating point value[1].
        [additional information: other options would be: X (1), Y (2), θ (4)]
        """
        R = self.__GetSomething('OUTP?3')
        if DEBUG:
            print("R: " + R)
        return float(R)

    def getPhi(self):
        """
        Query the value of θ (4). Returns ASCII floating point value[1].
        [additional information: other options would be: X (1), Y (2), R (3)]
        """
        phi = self.__GetSomething('OUTP?4')
        if DEBUG:
            print("Phi: " + phi)
        return float(phi)

    def getSens(self):
        """
        duplicate to method GetSens
        The SENS? command queries the sensitivity[1].

        i=0(≙2 nV/fA), i=1(≙5 nV/fA), i=2(≙10 nV/fA), i=3(≙20 nV/fA), i=4(≙50 nV/fA), i=5(≙100 nV/fA), i=6(≙200 nV/fA), 
        i=7(≙500 nV/fA), i=8(≙1 μV/pA), i=9(≙2 μV/pA), i=10(≙5 μV/pA), i=11(≙10 μV/pA), i=12(≙20 μV/pA), i=13(≙50 μV/pA),
        i=14(≙100 μV/pA), i=15(≙200 μV/pA), i=16(≙500 μV/pA), i=17(≙1 mV/nA), i=18(≙2 mV/nA), i=19(≙5 mV/nA), i=20(≙10 mV/nA),
        i=21(≙20 mV/nA), i=22(≙50 mV/nA), i=23(≙100 mV/nA), i=24(≙200 mV/nA), i=25(≙500 mV/nA), i=26(≙1 V/μA)
        """
        i = self.__GetSomething('SENS?')
        if DEBUG:
            print("Sens: " + i)
        return float(i)

    def getF(self):
        """
        duplicate to method GetRefFreq        

        The FREQ? query command will return the reference frequency 
        (in internal or external mode)[1]. 
        """
        fr = self.__GetSomething('FREQ?')
        if DEBUG:
            print("F: " + fr)
        return float(fr)

####################
# Instrument status

    def SerialPollDiagnostic(self):
        """
        I have no idea what this method is supposed to do (-> untested)
        """
        resp = self.__GetSomething('*STB?')

        SPB = int(resp)  # SPB ...serial poll byte

        # .....no command in progress
        ok = SPB & 1 | SPB & 2 | (not (SPB & 64))
        if (not ok):
            SPBbit0 = SPB & 0  # no data is beeing acquired
            SPBbit1 = SPB & 2  # no command execution in progress
            SPBbit2 = SPB & 4  # unmasked bit in error status byte set
            SPBbit3 = SPB & 8  # unmasked bit in LIA status byte set
            SPBbit4 = SPB & 16  # !!!! the interface output buffer is not empty
            SPBbit5 = SPB & 32  # unmasked bit in standard status byte set
            # SRQ has oThe FREQ? query command will return the reference frequency
            SPBbit6 = SPB & 64
            SPBbit7 = SPB & 128  # not in use
            if SPBbit2:
                print('unmasked bit in error status byte set')
                # may be subroutine call required
                ERRSbyte = self.__GetSomething('ERRS?')
                print('error-status byte: ', ERRSbyte)
            if SPBbit3:
                print('unmasked bit in LIA status byte set')
                # may be subroutine call required
                LIASbyte = self.__GetSomething('LIAS?')
                print('LIA-status byte: ', LIASbyte)
            if SPBbit4:
                self.SendString('REST')  # not shure that this will help
            if SPBbit5:
                # may be subroutine call required
                ESRbyte = self.__GetSomething('*ESR?')
                print('standard event-status byte: ', ESRbyte)
            if SPBbit6:
                # may be subroutine call required
                SPEbyte = self.__GetSomething('*SRE?')
                print('SRQ occurred SP enable register value ', SPEbyte)
        return SPB

# reference settings
    def SetRefRms(self, rms):
        """
        The SLVL x command sets the amplitude of the sine output.
        The parameter x is a voltage (real number of Volts). The value of x will
        be rounded to 0.002V. The value of x is limited to 0.004 ≤ x ≤ 5.000[1].  
        """
        # if rms < 0.004 or rms > 5.0:
        #    raise Exception("SetRefRms: parameter rms can only be set to values from 0.004 to 5.0")
        resp = self.__SetSomething('SLVL', rms)
        return resp

    def GetRefRms(self):
        """
        The SLVL? command queries the amplitude of the sine output.
        """
        rms = self.__GetSomething('SLVL?')
        return float(rms)

    def SetRefFreq(self, f):
        """
        The FREQ f command sets the frequency of the internal oscillator. This
        command is allowed only if the reference source is internal. The parame-
        ter f is a frequency (real number of Hz). The value of f will be rounded to
        5 digits or 0.0001 Hz, whichever is greater. The value of f is limited to
        0.001 ≤ f ≤ 102000. If the harmonic number is greater than 1, then the
        frequency is limited to nxf ≤ 102 kHz where n is the harmonic number[1].
        """
        # if f < 0.001 or f > 102000:
        #    raise Exception("SetRefFreq: parameter f can only be set to values from 0.001 to 102000.")
        resp = self.__SetSomething('FREQ', str(f))
        return resp

    def GetRefFreq(self):
        """
        duplicate to method getF

        The FREQ? query command will return the reference frequency 
        (in internal or external mode)[1].
        """
        f = self.__GetSomething('Freq?')
        return float(f)

    def SetRefPhas(self, phase):
        """
        The PHAS x command will set the phase shift to x. 
        The parameter x is the phase (real number of degrees).        
        The value of x will be rounded to 0.01°.
        The phase may be programmed from -360.00 ≤ x ≤ 729.99 and will be
        wrapped around at ±180°. For example, the PHAS 541.0 command will
        set the phase to -179.00° (541-360=181=-179)[1].
        """
        # if phase < -360.0 or phase > 729.99:
        #    raise Exception("SetRefPhas: parameter phase can only be set to values from -360.0 to 729.99")
        resp = self.__SetSomething('PHAS', str(phase))
        return resp

    def GetRefPhas(self):
        """
        The PHAS? command queries the reference phase shift[1].
        """
        phase = self.__GetSomething('PHAS?')
        return float(phase)

    def SetRefMode(self, refmod):
        """
        The FMOD i command sets the reference source. The parameter
        i selects internal (i=1) or external (i=0)[1].
        """
        if refmod not in (0, 1):
            raise Exception(
                "SetRefMode: parameter refmode can only be set to 0 (=external) or 1(=internal)")
        resp = self.__SetSomething('FMOD', str(refmod))
        return resp

    def __checkFractionalDigits(self, i, exception_text):
        """
        internal method checks if there are other numbers than 0 among the fractional digits
        """
        import decimal
        if "." in str(i):
            d = decimal.Decimal(i).as_tuple()
            preDecimalPlaces = len(d.digits) + d.exponent
            try:
                fractionalDigits = int(str(i)[(preDecimalPlaces + 1):])
            except:
                raise Exception(exception_text)
            if fractionalDigits != 0:
                raise Exception(exception_text)

    def GetRefMode(self):
        """
        The FMOD? command queries the reference source[1].
        refmod=0(≙external) or refmode=1(≙internal)
        """
        refmod = self.__GetSomething('FMOD?')
        return int(refmod)

    def SetRefHarm(self, harm):
        """
        The HARM i command sets the detection harmonic. This
        parameter is an integer from 1 to 19999. The HARM i command will set
        the lock-in to detect at the i th harmonic of the reference frequency. The
        value of i is limited by ixf ≤ 102 kHz. If the value of i requires a detection
        frequency greater than 102 kHz, then the harmonic number will be set to
        the largest value of i such that ixf ≤ 102 kHz[1].
        """
        # if harm < 1 or harm > 19999:
        #    raise Exception("harm can only be set to values from 1 to 19999")
        exception_text = "SetRefHarm: parameter harm has to be int or long from 1 to 19999"
        self.__checkFractionalDigits(harm, exception_text)
        try:
            harm = int(harm)
        except:
            raise Exception(exception_text)

        if not isinstance(harm, int):
            raise Exception(exception_text)
        resp = self.__SetSomething('HARM', str(harm))
        return resp

    def GetRefHarm(self):
        """
        The HARM? command queries the detection harmonic[1].
        """
        harm = self.__GetSomething('HARM?')
        return int(harm)

#input and filter
    def SetInputConfig(self, iconf):
        """
        The ISRC command sets the input configuration. The parameter
        i selects A (i=0), A-B (i=1), I (1 MΩ) (i=2) or I (100 MΩ) (i=3).

        Changing the current gain does not change the instrument sensitivity.
        Sensitivities above 10 nA require a current gain of 1 MΩ. Sensitivities
        between 20 nA and 1 μA automatically select the 1 MΩ current gain. At
        sensitivities below 20 nA, changing the sensitivity does not change the
        current gain[1].
        """
        if iconf not in (0, 1, 2, 3):
            raise Exception(
                "SetInputConfig: parameter iconf can only be set to value from 0 to 3\nA (iconf=0), A-B (iconf=1), I (1 MΩ) (iconf=2) or I (100 MΩ) (iconf=3)")
        resp = self.__SetSomething('ISRC', str(iconf))
        return resp

    def GetInputConfig(self):
        """
        The ISRC? command queries the input configuration[1].
        iconf=0 (≙A), iconf=1(≙A-B), iconf=2 (≙I(1 MΩ)) or iconf=3(≙I(100 MΩ))
        """
        iconf = self.__GetSomething('ISRC?')
        return int(iconf)

    def SetGNDConfig(self, gndconf):
        """
        The IGND command queries the input shield grounding[1]. The
        parameter gndconf selects Float (gndconf=0) or Ground (gndconf=1).
        """
        if gndconf not in (0, 1):
            raise Exception(
                "SetGNDConfig: parameter gndconf can only be 0(≙Float) or 1(≙Ground)")
        self.__SetSomething('IGND', gndconf)

    def GetGNDConfig(self):
        """
        The IGND? command queries the input shield grounding[1]. The
        gndconf=0(≙Float) or gndconf=1(≙Ground)
        """
        gndconf = self.__GetSomething('IGND?')
        return int(gndconf)

    def SetInputCoupling(self, icoup):
        """
        The ICPL i command sets the input coupling. 
        The parameter i selects AC (i=0) or DC (i=1)[1].
        """
        if icoup not in (0, 1):
            raise Exception(
                "SetInputCoupling: parameter icoup can only be 0(≙AC) or 1(≙DC)")
        resp = self.__SetSomething('ICPL', icoup)
        return resp

    def GetInputCoupling(self):
        """
        The ICPL? command queries the input coupling[1].
        icoup=0(≙AC) or icoup=1(≙DC)
        """
        icoup = self.__GetSomething('ICPL?')
        return int(icoup)

    def SetLineNotch(self, linotch):
        """
        The ILIN i command sets the input line notch filter status. The
        parameter i selects Out or no filters (i=0), Line notch in (i=1), 2xLine
        notch in (i=2) or Both notch filters in (i=3)[1].
        """
        if linotch not in (0, 1, 2, 3):
            raise Exception(
                "SetLineNotch: parameter linotch can only be set to 0(≙Out or no filters), 1(≙Line notch in), 2(≙2xLine notch in) or 3(≙Both notch filters in)")
        self.__SetSomething('ILIN', str(linotch))

    def GetLineNotch(self):
        """
        The ILIN? command queries the input line notch filter status[1].
        """
        linotch = self.__GetSomething('ILIN?')
        return int(linotch)

    def SetSens(self, i):
        """
        The SENS command sets the sensitivity[1].

        i=0(≙2 nV/fA), i=1(≙5 nV/fA), i=2(≙10 nV/fA), i=3(≙20 nV/fA), i=4(≙50 nV/fA), i=5(≙100 nV/fA), i=6(≙200 nV/fA), 
        i=7(≙500 nV/fA), i=8(≙1 μV/pA), i=9(≙2 μV/pA), i=10(≙5 μV/pA), i=11(≙10 μV/pA), i=12(≙20 μV/pA), i=13(≙50 μV/pA),
        i=14(≙100 μV/pA), i=15(≙200 μV/pA), i=16(≙500 μV/pA), i=17(≙1 mV/nA), i=18(≙2 mV/nA), i=19(≙5 mV/nA), i=20(≙10 mV/nA),
        i=21(≙20 mV/nA), i=22(≙50 mV/nA), i=23(≙100 mV/nA), i=24(≙200 mV/nA), i=25(≙500 mV/nA), i=26(≙1 V/μA)
        """
        exception_text = "SetSens: parameter i can only be set to int or long values from 0 to 26\n"
        exception_text += "i=0(≙2 nV/fA), i=1(≙5 nV/fA), i=2(≙10 nV/fA), i=3(≙20 nV/fA), i=4(≙50 nV/fA), i=5(≙100 nV/fA), i=6(≙200 nV/fA), "
        exception_text += "i=7(≙500 nV/fA), i=8(≙1 μV/pA), i=9(≙2 μV/pA), i=10(≙5 μV/pA), i=11(≙10 μV/pA), i=12(≙20 μV/pA), i=13(≙50 μV/pA), "
        exception_text += "i=14(≙100 μV/pA), i=15(≙200 μV/pA), i=16(≙500 μV/pA), i=17(≙1 mV/nA), i=18(≙2 mV/nA), i=19(≙5 mV/nA), i=20(≙10 mV/nA), "
        exception_text += "i=21(≙20 mV/nA), i=22(≙50 mV/nA), i=23(≙100 mV/nA), i=24(≙200 mV/nA), i=25(≙500 mV/nA), i=26(≙1 V/μA)"
        self.__checkFractionalDigits(i, exception_text)
        try:
            i = int(i)
        except:
            raise Exception(exception_text)
        if i < 0 or i > 26 or not(isinstance(i,  int)):
            raise Exception(exception_text)
        self.__SetSomething('SENS', i)

    def GetSens(self):
        """        
        duplicate to method getSens

        The SENS? command queries the sensitivity[1].

        i=0(≙2 nV/fA), i=1(≙5 nV/fA), i=2(≙10 nV/fA), i=3(≙20 nV/fA), i=4(≙50 nV/fA), i=5(≙100 nV/fA), i=6(≙200 nV/fA), 
        i=7(≙500 nV/fA), i=8(≙1 μV/pA), i=9(≙2 μV/pA), i=10(≙5 μV/pA), i=11(≙10 μV/pA), i=12(≙20 μV/pA), i=13(≙50 μV/pA),
        i=14(≙100 μV/pA), i=15(≙200 μV/pA), i=16(≙500 μV/pA), i=17(≙1 mV/nA), i=18(≙2 mV/nA), i=19(≙5 mV/nA), i=20(≙10 mV/nA),
        i=21(≙20 mV/nA), i=22(≙50 mV/nA), i=23(≙100 mV/nA), i=24(≙200 mV/nA), i=25(≙500 mV/nA), i=26(≙1 V/μA)
        """
        R = self.__GetSomething('SENS?')
        return int(R)

    def SetReserve(self, reserve):
        """
        The RMOD i command sets the reserve mode. The parameter i
        selects High Reserve (i=0), Normal (i=1) or Low Noise (minimum) (i=2).
        See in the manual-description of the [Reserve] key for the actual reserves for each
        sensitivity[1].
        """
        if reserve not in (0, 1, 2):
            raise Exception(
                "SetReserve: parameter reserve can only be set to the values 0(≙High Reserve), 1(≙Normal) or 2(≙Low Noise)")
        self.__SetSomething('RMOD', str(reserve))

    def GetReserve(self):
        """
        The RMOD? command queries the reserve mode[1].
        reserve=0(≙High Reserve), reserve=1(≙Normal) or reserve=2(≙Low Noise)
        """
        reserve = self.__GetSomething('RMOD?')
        return int(reserve)

    def SetTimeConst(self, i):
        """
        The OFLT i command sets the time constant[1].

        i=0(≙10 μs), i=1(≙30 μs), i=2(≙100 μs), i=3(≙300 μs), i=4(≙1 ms), i=5(≙3 ms), i=6(≙10 ms), 
        i=7(≙30 ms), i=8(≙100 ms), i=9(≙300 ms), i=10(≙1 s), i=11(≙3 s), i=12(≙10 s), i=13(≙30 s),
        i=14(≙100 s), i=15(≙300 s), i=16(≙1 ks), i=17(≙3 ks), i=18(≙10 ks), i=19(≙30 ks)
        use the method self.ConvertTimeconstantToi to convert your timeconstant to the needed parameter for this method

        Time constants greater than 30s may NOT be set if the harmonic x ref. frequency (detection frequency) exceeds 200 Hz. 
        Time constants shorter than the minimum time constant (based upon the filter slope and dynamic reserve) will set the 
        time constant to the minimum allowed time constant[1]. See the Gain and Time Constant operation section in the manual.
        """
        exception_text = "SetTimeConst: parameter i can only be set to values from 0 to 19\n"
        exception_text += "i=0(≙10 μs), i=1(≙30 μs), i=2(≙100 μs), i=3(≙300 μs), i=4(≙1 ms), i=5(≙3 ms), i=6(≙10 ms), "
        exception_text += "i=7(≙30 ms), i=8(≙100 ms), i=9(≙300 ms), i=10(≙1 s), i=11(≙3 s), i=12(≙10 s), i=13(≙30 s), "
        exception_text += "i=14(≙100 s), i=15(≙300 s), i=16(≙1 ks), i=17(≙3 ks), i=18(≙10 ks), i=19(≙30 ks)"
        self.__checkFractionalDigits(i, exception_text)
        try:
            i = int(i)
        except:
            raise Exception(exception_text)
        if i < 0 or i > 19 or not(isinstance(i, int)):
            raise Exception(exception_text)
        self.__SetSomething('OFLT', i)

    def GetTimeConst(self):
        """
        The OFLT? command queries the time constant[1].
        use the method self.ConvertiToTimeconstant to convert the return-value of this method to the actual timeconstant 
        """
        tc = self.__GetSomething('OFLT?')
        # 1e-5 * 10**np.floor(int(tc)/2) * (1+2*(int(tc)%2)) #numerischer Wert
        return int(tc)

    def SetSlope(self, slope):
        """
        The OFSL i command setsthe low pass filter slope. The
        parameter slope selects 6 dB/oct (slope=0), 12 dB/oct (slope=1), 18 dB/oct (slope=2) or
        24 dB/oct (slope=3)[1].
        """
        exception_text = "SetSlope: parameter slope can only be set to the values 0(≙6 dB/oct), 1(≙12 dB/oct), 2(≙18 dB/oct) or 3(≙24 dB/oct)."
        self.__checkFractionalDigits(slope, exception_text)
        try:
            slope = int(slope)
        except:
            raise Exception(exception_text)
        if slope < 0 or slope > 3 or not(isinstance(slope, int)):
            raise Exception(exception_text)
        self.__SetSomething('OFSL', slope)

    def GetSlope(self):
        """
        The OFSL? command queries the low pass filter slope[1].
        slope=0(≙6 dB/oct), slope=1(≙12 dB/oct), slope=2(≙18 dB/oct) or
        slope=3(≙24 dB/oct)
        """
        slope = self.__GetSomething('OFSL?')
        return int(slope)

    def SetSyncFilter(self, sync):
        """
        The SYNC i command sets the synchronous filter status. The
        parameter i selects Off (i=0) or synchronous filtering below 200 Hz (i=1).
        Synchronous filtering is turned on only if the detection frequency (refer-
        ence x harmonic number) is less than 200 Hz[1].
        """
        exception_text = "SetSyncFilter: parameter sync can only be set to 0(≙Off) or 1(≙synchronous filtering below 200 Hz)."
        self.__checkFractionalDigits(sync, exception_text)
        try:
            sync = int(sync)
        except:
            raise Exception(exception_text)
        if sync < 0 or sync > 1 or not(isinstance(sync, int)):
            raise Exception(exception_text)
        self.__SetSomething('SYNC', sync)

    def GetSyncFilter(self):
        """
        The SYNC? command queries the synchronous filter status[1].
        sync=0(≙Off) or sync=1(≙synchronous filtering below 200 Hz).
        """
        sync = self.__GetSomething('SYNC?')
        return int(sync)

    def SetDisplay(self, channel, j, ratio=0):
        """
        The DDEF i, j, k command selects the CH1 and CH2 displays. The parameter
        channel selects CH1 (channel=1) or CH2 (channel=2) and is required. 
        This command sets channel i to parameter j with ratio k as listed below.
            CH1 (i=1)       4 CH2 (i=2)       
        j   display     j   display
        0   X           0   Y
        1   R           1   θ
        2   X Noise     2   Y Noise
        3   Aux In 1    3   Aux In 3
        4   Aux In 2    4   Aux In 4
        k   ratio       k   ratio
        0   none        0   none
        1   Aux In 1    1   Aux In 3
        2   Aux In 2    2   Aux In 4
        [1]    
        """
        ch = str(channel)
        k = str(j)
        rat = str(ratio)
        Cmd = 'DDEF' + ch + ',' + k + ',' + rat
        self.SendString(Cmd)
        return

    def GetDisplay(self, channel=1):
        """
        The DDEF? i command queries the display and ratio of display i. The
        returned string contains both j and k separated by a comma. For exam-
        ple, if the DDEF? 1 command returns "1,0" then the CH1 display is R
        with no ratio[1].
        """
        resp = self.__GetSomething('DDEF? ' + str(channel))
        [j, ratio] = resp.rsplit(',')
        return [j, ratio]

    def SetInterface(self, GPIB=True, RS232=False):
        """
        The OUTX i command sets the output interface to RS232 (i=0) or GPIB(i=1).
        The OUTX i command should be sent before any query com-
        mands to direct the responses to the interface in use[1].
        """
        if GPIB:
            Cmd = 'OUTX 1'  # sets te output interface to GPIB
        else:
            Cmd = 'OUTX 0'  # sets the output interface to RS232
        self.SendString(Cmd)
        return

    def GetInterface(self, GPIB=False, RS232=False):
        """
        The OUTX? command queries the interface[1].
        Interface=0(≙RS232) or Interface=1(≙GPIB).
        """
        Ifc = self.__GetSomething('OUTX?')
        if int(Ifc) == 1:
            Interface = 'GPIB'
        else:
            Interface = 'RS232'
        return int(Ifc), Interface

    def SetDisableRemoteLockoutState(self, On=True):
        """
        In general, every GPIB interface command will put the SR830 into the
        REMOTE state with the front panel deactivated. To defeat this feature,
        use the OVRM 1 command to overide the GPIB remote. In this mode, the
        front panel is not locked out when the unit is in the REMOTE state. The
        OVRM 0 command returns the unit to normal remote operation[1].
        """
        if On:
            Cmd = 'OVRM 1'  # Front panel is not locked out
        else:
            Cmd = 'OVRM 0'  # Front panel is locked out
        self.SendString(Cmd)
        return

    def SetKlickOn(self, On=False):
        """
        The KCLK i command sets the key click On (i=1) or Off (i=0) state[1].
        """
        if On:
            Cmd = 'KCLK 1'
        else:
            Cmd = 'KCLK 0'
        self.SendString(Cmd)
        return

    def GetKlickOn(self, On=False):
        """
        The KCLK i command queries the key[1].
        """
        KlickOn = self.__GetSomething('KCLK?')
        return int(KlickOn)

    def SetAlarm(self, On=False):
        """
        The ALRM i command sets the alarm On (i=1) or Off (i=0) state[1].
        """
        if On:
            Cmd = 'ALRM 1'
        else:
            Cmd = 'ALRM 0'
        self.SendString(Cmd)
        return

    def GetAlarm(self, On=False):
        """
        The ALRM? command queries the alarm[1] 
        Alarm=1(≙On) or Alarm=0(≙Off).
        """
        Alarm = self.__GetSomething('ALRM?')
        return int(Alarm)

    def SaveSettings(self, BufferAddress=1):
        """
        The SSET i command saves the lock-in setup in setting buffer i (1<i<9).
        The setting buffers are retained when the power is turned off[1].
        """
        self.__SetSomething('SSET', BufferAddress)

    def ReactivateSettings(self, BufferAddress=1):
        """
        The RSET i command recalls the lock-in setup from setting buffer i
        (1≤i≤9). Interface parameters are not changed when a setting buffer is
        recalled with the RSET command. If setting i has not been saved prior to
        the RSET i command, then an error will result[1].
        """
        self.__SetSomething('RSET', BufferAddress)

    def SetAutoGain(self):
        """
        The AGAN command performs the Auto Gain function. This command is
        the same as pressing the [Auto Gain] key. Auto Gain may take some
        time if the time constant is long. AGAN does nothing if the time constant
        is greater than 1 second. Check the command execution in progress bit
        in the Serial Poll Status Byte (bit 1) to determine when the function is
        finished[1].
        """
        cmd = 'AGAN'
        self.SendString(cmd)
        return

    def SetFrontOutputSource(self, which=None, Type=None):
        """
        The FPOP i,j command sets the front panel (CH1 and CH2) output sources. 
        The parameter i selects CH1 (i=1) or CH2 (i=2) and is required. 
        The FPOP i, j command sets output i to quantity j where j is
        listed below.
          CH1 (i=1)                 4 CH2 (i=2)       
        j   output quantity     j   output quantity
        0   CH 1 Display        0   CH 2 Display
        1   X                   1   Y
        [1]
        """
        cmd = 'FPOP ' + str(which) + ',' + str(Type)
        self.SendString(cmd)

    def GetFrontOutputSource(self, which=None):
        """
        The FPOP? command queries the front panel (CH1 and CH2) output sources[1].
        """
        resp = self.__GetSomething('FPOP?' + str(which))
        if str(resp) == 0:
            Type = 'Display Channel ' + str(which)
        else:
            if which == 1:
                Type = 'X'
            else:
                Type = 'Y'
        return Type

    def GetOutputOffsetAndExpand(self, i):
        """
        The OEXP? i command queries the output offsets and expand of quantity i.
        The parameter i selects X (i=1), Y (i=2) or R (i=3) and is required.
        The returned string contains both the offset and
        expand separated by a comma. For example, if the OEXP? 2 command
        returns "50.00,1" then the Y offset is 50.00% and the Y expand is 10.
        Setting an offset to zero turns the offset off. Querying an offset which is
        off will return 0% for the offset value[1].
        """
        exception_text = "GetOutputOffsetAndExpand: parameter i can only be 1(≙X), 2(≙Y) or 3(≙R)"
        self.__checkFractionalDigits(i, exception_text)
        try:
            i = int(i)
        except:
            raise Exception(exception_text)
        if i < 1 or i > 3 or not(isinstance(i, int)):
            raise Exception(exception_text)

        Type = ['X', 'Y', 'R']
        cmd = 'OEXP? ' + str(i)
        resp = self.__GetSomething(cmd)
        [offset, expand] = resp.rsplit(',')
        return Type[i-1], offset, expand

    def SetOutputOffsetAndExpand(self, Param, Offset, Expand):
        """
        The OEXP i, x, j command will set the offset and expand for quantity i. 
        This command requires BOTH x and j.
        The parameter i selects X (i=1), Y (i=2) or R (i=3) and is required. The
        parameter x is the offset in percent (-105.00 ≤ x ≤ 105.00). The parame-
        ter j selects no expand (j=0), expand by 10 (j=1) or 100 (j=2)[1].
        """
        cmd = 'OEXP ' + str(Param) + ',' + str(Offset) + ',' + str(Expand)
        self.SendString(cmd)

    def SetAutoReserve(self):
        """
        The ARSV command performs the Auto Reserve function. This com-
        mand is the same as pressing the [Auto Reserve] key. Auto Reserve
        may take some time. Check the command execution in progress bit in
        the Serial Poll Status Byte (bit 1) to determine when the function is
        finished[1].
        """
        cmd = 'ARSV'
        self.SendString(cmd)

    def SetAutoPhase(self):
        """
        The APHS command performs the Auto Phase function. This command
        is the same as pressing the [Auto Phase] key. The outputs will take many
        time constants to reach their new values. Do not send the APHS com-
        mand again without waiting the appropriate amount of time. If the phase
        is unstable, then APHS will do nothing. Query the new value of the phase
        shift to see if APHS changed the phase shift[1].
        """
        cmd = 'APHS'
        self.SendString(cmd)

    def SetAutoOffset(self, which):
        """
        The AOFF i command automatically offsets X (i=1), Y (i=2) or R (i=3) to
        zero. The parameter i is required. This command is equivalent to press-
        ing the [Auto Offset] keys[1].
        """
        exception_text = "SetAutoOffset: parameter which can only be 1(≙X), 2(≙Y) or 3(≙R)"
        self.__checkFractionalDigits(which, exception_text)
        try:
            which = int(which)
        except:
            raise Exception(exception_text)
        if which < 1 or which > 3 or not(isinstance(which, int)):
            raise Exception(exception_text)

        self.__SetSomething('AOFF', which)

    def SetDataSampleRate(self, rate=4):
        """
        The SRAT i command sets the data sample rate. The parame-
        ter i selects the sample rate listed below.
        i   quantity    i   quantity
        0   62.5 mHz    8   16 Hz
        1   125 mHz     9   32 Hz
        2   250 mHz    10   64 Hz
        3   500 mHz    11   128 Hz
        4   1 Hz       12   256 Hz
        5   2 Hz       13   512 Hz
        6   4 Hz       14   Trigger
        7   8 Hz
        [1]
        """
        self.__SetSomething('SRAT', rate)

    def GetDataSampleRate(self, rate=None):
        """
        The SRAT? command queries the data sample rate[1].
        """
        Rate = self.__GetSomething('SRAT?')
        return int(Rate)

    def SetEndOfBuffer(self, kind=None):
        """
        The SEND i command sets the end of buffer mode. The param-
        eter i selects 1 Shot (i=0) or Loop (i=1). If Loop mode is used, make sure
        to pause data storage before reading the data to avoid confusion about
        which point is the most recent[1].
        """
        if kind not in (0, 1):
            raise Exception(
                "SetEndOfBuffer: parameter kind can only be 0(≙Shot) or 1(≙Loop)")
        self.__SetSomething('SEND', kind)

    def GetEndOfBuffer(self, kind=None):
        """
        The SEND? command queries the end of buffer mode[1].
        """
        Kind = self.__GetSomething('SEND?')
        return Kind

    def Trigger(self):
        """
        The TRIG command is the software trigger command. This command
        has the same effect as a trigger at the rear panel trigger input[1].
        """
        self.SendString('TRIG')

    def SetTriggerStartMode(self, kind):
        """
        The TSTR i command sets the trigger start mode. The parameter 
        i=1 selects trigger starts the scan and i=0 turns the trigger start feature off.
        """
        if kind not in (0, 1):
            raise Exception(
                "SetTriggerStartMode: parameter kind can only be 0(≙trigger starts the scan) or 1(≙turns the trigger start feature off)")
        self.__SetSomething('TSTR', kind)

    def GetTriggerStartMode(self):
        """
        The TSTR? command queries the trigger start mode[1].
        """
        Kind = self.__GetSomething('TSTR?')
        return int(Kind)

    def Start(self):
        """
        The STRT command starts or resumes data storage. STRT is ignored if
        storage is already in progress[1].
        """
        self.SendString('STRT')

    def Pause(self):
        """
        The PAUS command pauses data storage. If storage is already paused
        or reset then this command is ignored[1].
        """
        self.SendString('PAUS')

    def SetTriggerSlope(self, value):
        """
        The RSLP command sets the reference trigger when using the
        external reference mode. The parameter i selects sine zero crossing
        (i=0), TTL rising edge (i=1), , or TTL falling edge (i=2). At frequencies
        below 1 Hz, the a TTL reference must be used[1].
        """
        if value not in (0, 1, 2):
            raise Exception(
                "SetTriggerSlope: parameter value can only be 0(≙sine zero crossing), 1(≙TTL rising edge/Pos edge) or 2(≙TTL falling edge/neg edge)")
        snd = "RSLP%i" % value
        self.SendString(snd)

    def iToSlope(self, i):
        """
        converts the response returned by GetTriggerSlope to the actual slope
        """
        options = {0: 'Sine',
                   1: 'Pos edge',
                   2: 'neg edge'
                   }
        return options[int(i.strip())]

    def GetTriggerSlope(self):
        """
        The RSLP? command queries the reference trigger when using the
        external reference mode.
        use the method self.iToSlope to convert the response of this method to the actual slope
        """
        resp = self.__GetSomething('RSLP?')
        return resp

    def Reset(self):
        """
        Reset the unit to its default configurations[1].
        """
        self.SendString('*RST')

    def ResetDataBuffers(self):
        """
        The REST command resets the data buffers. The REST command can
        be sent at any time - any storage in progress, paused or not, will be
        reset. This command will erase the data buffer[1].
        """
        self.SendString('REST')

    def GetSelectedOutput(self, which):
        """
        The OUTP? i command reads the value of X, Y, R or θ. The parameter
        i selects X (i=1), Y (i=2), R (i=3) or θ (i=4). Values are returned as ASCII
        floating point numbers with units of Volts or degrees. For example, the
        response might be "-1.01026". This command is a query only command[1].
        """
        if which not in (1, 2, 3, 4):
            raise Exception(
                "GetSelectedOutput: parameter which can only be 1(≙X),2(≙Y),3(≙R) or 4(≙θ)")
        Value = self.__GetSomething('OUTP?' + str(which))
        if which == 1:
            Type = 'X'
        elif which == 2:
            Type = 'Y'
        elif which == 3:
            Type = 'R'
        elif which == 4:
            Type = 'θ'

        return [float(Value), Type]

    def GetSelectedDisplayValue(self, which):
        """
        The OUTR? i command reads the value of the CH1 or CH2 display.
        The parameter i selects the display (i=1 or 2). Values are returned as
        ASCII floating point numbers with units of the display. For example, the
        response might be "-1.01026". This command is a query only command[1].
        """
        if which not in (1, 2):
            raise Exception(
                "GetSelectedDisplayValue: parameter which can only be 1(≙CH1) or 2(≙CH2)")
        Value = self.__GetSomething('OUTR?' + str(which))
        time.sleep(0.2)
        resp = float(Value)
        if DEBUG:
            print("GetSelectedDisplayValue: " + Value)
        return resp

    def __check_snap(self, param):
        """
        internal function used by method SNAP
        ensures that the SNAP-params are correct
        """
        if param not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
            raise Exception(
                "SNAP: Parameters can only be 1(≙X), 2(≙Y), 3(≙R), 4(≙θ), 5(≙Aux In 1), 6(≙Aux In 2), 7(≙Aux In 3), 8(≙Aux In 4), 9(≙Reference Frequency), 10(≙CH1 display) or 11(≙CH2 display)")

    def SNAP(self, Param1, Param2, Param3=None, Param4=None, Param5=None, Param6=None):
        """
        The SNAP? command records the values of either 2, 3, 4, 5 or 6 param-
        eters at a single instant. For example, SNAP? is a way to query values of
        X and Y (or R and θ) which are taken at the same time. This is important
        when the time constant is very short. Using the OUTP? or OUTR? com-
        mands will result in time delays, which may be greater than the time con-
        stant, between reading X and Y (or R and θ).
        The SNAP? command requires at least two parameters and at most six
        parameters. The parameters i, j, k, l, m, n select the parameters below.

        i,j,k,l,m,n     parameter
        1               X
        2               Y
        3               R
        4               θ
        5               Aux In 1
        6               Aux In 2
        7               Aux In 3
        8               Aux In 4
        9               Reference Frequency
        10              CH1 display
        11              CH2 display
        The requested values are returned in a single string with the values sep-
        arated by commas and in the order in which they were requested. For
        example, the SNAP?1,2,9,5 will return the values of X, Y, Freq and
        Aux In 1. These values will be returned in a single string such as
        "0.951359,0.0253297,1000.00,1.234".
        The first value is X, the second is Y, the third is f, and the fourth is
        Aux In 1.
        The values of X and Y are recorded at a single instant. The values of R
        and θ are also recorded at a single instant. Thus reading X,Y OR R,θ
        yields a coherent snapshot of the output signal. If X,Y,R and θ are all
        read, then the values of X,Y are recorded approximately 10μs apart from
        R,θ. Thus, the values of X and Y may not yield the exact values of R and
        θ from a single SNAP? query.
        The values of the Aux Inputs may have an uncertainty of up to 32μs. The
        frequency is computed only every other period or 40 ms, whichever is
        longer.

        The SNAP? command is a query only command. The SNAP? command
        is used to record various parameters simultaneously, not to transfer data
        quickly[1].
        """
        self.__check_snap(Param1)
        self.__check_snap(Param2)
        Cmdstr = 'SNAP?' + ' ' + str(Param1) + ',' + str(Param2)
        if Param3 != None:
            self.__check_snap(Param3)
            Cmdstr += ',' + str(Param3)
        if Param4 != None:
            self.__check_snap(Param4)
            Cmdstr += ',' + str(Param4)
        if Param5 != None:
            self.__check_snap(Param5)
            Cmdstr += ',' + str(Param5)
        if Param6 != None:
            self.__check_snap(Param6)
            Cmdstr += ',' + str(Param6)

        resp = self.__GetSomething(Cmdstr)

        if Param3 is None:  # no value, just the command string to query
            Val6 = None
            Val5 = None
            Val4 = None
            Val3 = None
            [Val1, Val2] = resp.rsplit(',')
        elif Param4 is None:
            Val6 = None
            Val5 = None
            Val4 = None
            [Val1, Val2, Val3] = resp.rsplit(',')
        elif Param5 is None:
            Val6 = None
            Val5 = None
            [Val1, Val2, Val3, Val4] = resp.rsplit(',')
        elif Param6 is None:
            Val6 = None
            [Val1, Val2, Val3, Val4, Val5] = resp.rsplit(',')
        else:
            [Val1, Val2, Val3, Val4, Val5, Val6] = resp.rsplit(',')

        return Val1, Val2, Val3, Val4, Val5, Val6, Param1, Param2, Param3, \
            Param4, Param5, Param6

    def GetAuxValue(self, number):
        """
        The OAUX? command reads the Aux Input values. The parameter i
        selects an Aux Input (1, 2, 3 or 4) and is required. The Aux Input voltages
        are returned as ASCII strings with units of Volts. The resolution is
        1/3 mV. This command is a query only command[1].
        """
        if number not in (1, 2, 3, 4):
            raise Exception(
                "GetAuxValue: parameter number can only be 1(≙Aux Input 1), 2(≙Aux Input 2), 3(≙Aux Input 3) or 4(≙Aux Input 4)")
        OutAux = self.__GetSomething('OAUX?' + str(number))
        return float(OutAux), number

    def GetOccupiedBuffer(self):
        """
        The SPTS? command queries the number of points stored in the buffer.
        Both displays have the same number of points. If the buffer is reset, then
        0 is returned. Remember, SPTS? returns N where N is the number of
        points - the points are numbered from 0 (oldest) to N-1 (most recent).
        The SPTS? command can be sent at any time, even while storage is in
        progress. This command is a query only command[1].
        """
        n = self.__GetSomething('SPTS?')
        return int(n)

# commented by WilHo, because this method uses GetOccupiedBuffer with parameter 'which',
# but SPTS? is a query only command for further information see the programming manual
#    def GetChannelBufferPoints(self,which,length):
#        if which not in (1,2):
#            raise Exception("which has to be 1 or 2")
#        if length <= 0:
#            raise Exception("Length hast to be >= 0")
#        length = int(self.GetOccupiedBuffer(which)) - 1
# DataBuffer = [((0:length)];
#        DataBuffer = []
#        for j in range(0,length):
#            cmd = 'TRCA? '+str(which)+',' + str(j) + ',1'
#            DataBuffer[j] = self.SetOrCheckSomething(cmd, None,0, length, False)
#        return DataBuffer[:]

    def close(self):
        '''
        Close the connection to the Instrument, return controle to instruments        
        controles and switch off output
        '''
        if sys.platform.startswith('win'):
            self.visa_instr.close()
        elif sys.platform.startswith('lin'):
            self.inst.clear()  # close() not implemented in Gpib.py


OUT_CLASS = liaSR830
