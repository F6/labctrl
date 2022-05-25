# Web API Servers for Lab Control

This directory contains all the web api servers for simplifing
control of lab instruments from different suppliers.

All of the servers are self-contained and can be used independently.

Some instruments like Topas and Zurich Instrument UHF already provides
good web APIs, however they are quite complicated for simple tasks and
may require additional authentication. For my convenience some proxy
code is written for the most used APIs so that it is tailored for our
needs.


## Port Assignments

To avoid conflict with existing APIs in our lab, different ports are assigned
to different server or proxies. If desired, the port can be changed in the
corresponding .bat files.

The "port" section in configs also needs to be changed if the server port has been altered

### Defaults

* Linear Stages:

        PMC48MT6            5000
        USB1020             5001
        CDHD2               5002
        AeroTech_THz        5003
        AeroTech_NView      5004
        CRD507              5005
        ETHGASN             5048

    <!-- 5006 used by bokeh server -->

* CCD and CMOS cameras:

        EMCCD               5007
        ToupCam             5008

* Monochromers:

        7IMSU               5009
        crd507_sigmakoki    5010

* Shutter Controllers:

        psTopasExit         5011
        fsTopasExit         5012

* Lock-in Amplifiers, Boxcar Averagers and Balanced Detectors:

        ziUHF               5013
        SR830               5014
    
* Digital single point detectors - Photodiodes and SiPM(MPPC):

        SiPMSelfMade1       5015
        SiPM4kHz            5022
    
* Linear CCD:

        TCD1304             5016
    
* Thermostats:

        TEC12706            5017

* Optical Parametric Amplifiers:

        Topas_ps            5018
        Topas_60fs          5019
        Topas_120fs         5020
        NOPA_SelfMade       5021
    
* Precision Voice Coil Stages and Piezo Flexures:

        PI-VoiceCoil10nm    5023
        PiezoController     5024
    
* Acousto-optic programmable dispersive filters and Pulse shapers:

        Dazzler             5025
        LCD-PS-SelfMade1    5026
    
* Oscilloscopes:

        Rigol               5027
    
* Spectrometers:

        FX2000              5028
    
* OpticalPowerMeters:

        ThorlabsSmall       5029
        ThorlabsLarge       5030
    
* Digital Multimeters:

        Victor              5031
    
* Programmable Power Supplies:

        Rigol3Ch            5032

* Trigger Signal Multiplexer/Modulator:

        mod_esp32           5033
    
* Atomic clocks and Precision delay units:

        rbclock             5034
        digitaldelay1       5035
    
* Pressure Gauges:

        mcbj_vac_chamber1   5036
        mcbj_argon          5037
    
* Electromagnetic Valves:

        mcbj1               5038

* Injection Pumps:

        pump3ch             5039

* Hall Probes:

        guochan1            5040
    
* Humidity Sensor and Controllers:

        dht                 5041
        humid               5042

* Software Defined Radio Transmitters and Receivers:

        sdr1                5043
        RFNoiseMonitor      5045

* Arbitrary Waveform Generators:

        Rigol               5044
    
* Optical Filter Arrays:

        kerrgate6           5045

* Flowmeters:

        dropmeter           5046

* Digital Pumps:

        MasterFlexLS        5047
