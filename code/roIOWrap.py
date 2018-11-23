#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

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
        pass

    def setSensorType(self, IFaceNumber, IFacePortNo, IFacePortType):
        pass

    def getSensorValue(self, IFaceNumber, IFacePortNo):
        pass

    def setOutputType(self, IFaceNumber, IFacePortNo, IFacePortType):
        pass

    def setOutputValue(self, IFaceNumber, IFacePortNo, IFacePortSettings):
        pass
