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
        wList, oList = wire.getObjectWireList()
        self.addNewWireObject(wList, oList)
        self._wires.append(wire)

    def addNewWireObject(self, wList, oList):
        """Generate a new Object with the dynamic-id and the wire connecting from the dynamic point to the 'begin' of the wire"""
        # generate a set of new wires
        for wireDat in wList:
            wireNew = RoboProWire()
            wireNew._type = wireDat["type"] + "Helper"
            wireNew._begin = wireDat["wireinput"]
            wireNew._end = wireDat["wireoutput"]
            wireNew._points = [
                {"id": "autogen", "name": "begin", "type": "flowwireinput", "resolve": wireNew._begin},
                {"id": "autogen", "name": "end", "type": "flowwireoutput", "resolve": wireNew._end}
            ]
            self._wires.append(wireNew)
        # generate a set of dummy-objects
        for objDat in oList:
            objNew = RoboProObject()
            objNew._type = objDat["type"]
            for objDatPin in objDat["pin"]:
                dat = {
                    "id": objDatPin["id"],
                    "name": objDatPin["type"],
                    "pinclass":  ""
                }
                objNew._pins.append(dat)
            self._objects.append(objNew)


    def buildGraph(self):
        for obj in self._objects:
            print("OBJ", obj._type)
            for pin in obj._pins:
                print(" >", "ID" + pin["id"], pin["pinclass"], pin["name"])
        for wire in self._wires:
            print("WIR", wire._type)
            for point in wire._points:
                print(" |", "ID" + point["id"], "RE" + point["resolve"], point["type"])

    def run(self):
        pass
