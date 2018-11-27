#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import ftrobopy
import time

__author__     = "Leon Schnieber"
__copyright__  = "Copyright 2018"
__credits__    = "fischertechnik GmbH"
__maintainer__ = "Leon Schnieber"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"


class RoboProIOWrap(object):
    """
    This class handles all communication between the main library and the IOs of
    the different controllers. It can be modified if another controller-library
    is used.
    """


    def __init__(self):
        self.ifaces = {}
        self.ifaces["IF1"] = ftrobopy.ftrobopy("192.168.7.2")
        time.sleep(0.5)

    def setSensorType(self, IFaceNumber, IFacePortNo, IFacePortType):
        pass

    def getSensorValue(self, IFaceNumber, IFacePortNo, IFacePortMode):
        """
        IFaceNumber-Values:
        IF1 = Master

        IFacePortNo-Values:
        I1 = 160
        I2 = 161
        …
        I8 = 167

        IFacePortMode-Values:
        0  = D 10V   Sensor-Type  6   (Spursensor)
        1  = D 5k    Sensor-Types 1-3 (Taster, Fototransitor, Reed-Kontakt)
        3  = A 10V   Sensor-Type  8   (Farbsensor)
        4  = A 5k    Sensor-Types 4-5 (NTC-Widerstand, Fotowiderstand)
        10 = Ultra…  Sensor-Type  7   (Abstandssensor)
        """
        iface = self.ifaces[IFaceNumber]
        if IFacePortMode == 1:  # digital 5k
            sensor = iface.input(IFacePortNo)
            value = sensor.state()
        elif IFacePortMode == 0: # spursensor
            sensor = iface.trailfollower(IFacePortNo)
            value = sensor.state()
        elif IFacePortMode == 3: # farbsensor
            sensor = iface.colorsensor(IFacePortNo)
            value = sensor.value()
        elif IFacePortMode == 4: # analog 5k
            sensor = iface.resistor(IFacePortNo)
            value = sensor.value()
        elif IFacePortMode == 10: # ultrasonic
            sensor = iface.ultrasonic()
            value = sensor.distance()
        return value

    def setOutputType(self, IFaceNumber, IFacePortNo, IFacePortType):
        pass

    def setOutputValue(self, IFaceNumber, IFacePortNo, IFacePortSettings):
        """
        Values of IFaceNumber:
        IF1 = Master
        …

        IFacePortNo-Values:
        0   = M1
        1   = M2
        …
        3   = M4

        IFacePortSettings: (dict)
        ["commandType"]   Language dependent set of commands.
        ["value"]         Ranges from 0 to 512

        List of availiable Command-types:
        "cw"   = CW Mot   (v=n)
        "ccw"  = CCW Mot  (v=n)
        "Stop" = Stop Mot (v=0)
        optionally, not known yet
        "On"   = On IO    (v=n)
        "Off"  = Off IO   (v=0)
        """
        iface = self.ifaces[IFaceNumber]
        val = int(IFacePortSettings["value"])
        if val > 512:
            val = 512
        if IFacePortNo >= 0 and IFacePortNo <= 3:
            output = iface.motor(IFacePortNo+1)
            print(IFacePortNo, val, IFacePortSettings["commandType"])
            if IFacePortSettings["commandType"] in ["Links", "ccw"]:
                output.setSpeed(-val)
            else:
                output.setSpeed(val)
            if "distance" in IFacePortSettings:
                if "syncTo" in IFacePortSettings:
                    output.setDistance(
                        IFacePortSettings["distance"],
                        syncto=iface.motor(IFacePortSettings["syncTo"]+1)
                    )
                else:
                    output.setDistance(IFacePortSettings["distance"])
        if "sleep" in IFacePortSettings and "distance" in IFacePortSettings:
            while output.getCurrentDistance() < IFacePortSettings["distance"]:
                time.sleep(0.01)
            output.stop()
