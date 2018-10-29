#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup
from roObject import RoboProObject
from roWire import RoboProWire

__author__     = "Leon Schnieber"
__copyright__  = "Copyright 2018"
__credits__    = "fischertechnik GmbH"
__maintainer__ = "Leon Schnieber"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"


class RoboProSubroutine(object):
    """
    The subroutineObject handles all wires and objects inside a subroutine in-
    stanciated by the RoboProProgram-Class.
    """
    objectTypeList = [
        "ftProProcessStart",
        "ftProProcessStop",
        "ftProFlowIf",
        "ftProDataIn",
        "ftProDataOutDual",
        "ftProDataMssg"
    ]

    wireTypeList = [
        "ftProFlowWire",
        "ftProDataWire"
    ]

    def __init__(self, subroutineXmlSoup):
        self._objects = []
        self._wires = []
        self._subroutineRaw = subroutineXmlSoup
        self.parse()

    def parse(self):
        objectsRaw = []
        # collect all objects in the xml
        for objectType in self.objectTypeList:
            data = self._subroutineRaw.find_all("o", attrs={
                "classname": objectType
            })
            for objectRaw in data:
                self.addNewObject(objectRaw)

        wiresRaw = []
        # collect all wires in the xml
        for wireType in self.wireTypeList:
            data = self._subroutineRaw.find_all("o", attrs={
                "classname": wireType
            })
            for wireRaw in data:
                self.addNewWire(wireRaw)


    def addNewObject(self, objRaw):
        """ Instanciates a new RoboProObject to be later used"""
        obj = RoboProObject(objRaw)
        self._objects.append(obj)

    def addNewWire(self, wireRaw):
        wire = RoboProWire(wireRaw)
        for wireobject in wire.getObjectList():
            self.addNewWireObject(wireobject)
        self._wires.append(wire)

    def addNewWireObject(self, wireobject):
        """Generate a new Object with the dynamic-id and the wire connecting from the dynamic point to the 'begin' of the wire"""
        obj = RoboProObject()
        obj._type = "WireNodeDataOrFlow"
        self._objects.append(obj)

    def buildGraph(self):
        pass

    def run(self):
        pass
