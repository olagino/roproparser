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
        # Start-Stop-Blocks
        "ftProProcessStart",
        "ftProProcessStop",
        "ftProFlowIf",
        # Data transmission
        "ftProDataIn",
        "ftProDataOutDual",
        # = Send stuff-Command
        "ftProDataMssg",
        "ftProFlowWaitChange",
        # Subroutine-Specific-Blocks
        "ftProSubroutineFlowIn",
        "ftProSubroutineFlowOut",
        "ftProSubroutineDataIn",
        "ftProSubroutineDataOut",
        # Variable and stuff
        "ftProDataVariable",
        "ftProDataConst",
        "ftProDataOprt", # operator
        ""
    ]

    wireTypeList = [
        "ftProFlowWire",
        "ftProDataWire"
    ]

    def __init__(self, subroutineXmlSoup):
        self._objects = []
        self._wires = []
        self._subroutineRaw = subroutineXmlSoup
        self._connectionChains = []
        self._connectionFragments = []
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
            wireNew._wireinput = wireDat["wireinput"]
            wireNew._wireoutput = wireDat["wireoutput"]
            wireNew._points = [
                {"id": "autogen", "name": "begin", "type": "flowwireinput", "resolve": wireNew._wireinput},
                {"id": "autogen", "name": "end", "type": "flowwireoutput", "resolve": wireNew._wireoutput}
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

    def _followWire(self, inputID):
        """
        The _followWire function takes an input-ID and follows the wire to the
        next element in the chain and returns the ID of the Block-Input
        """
        for wire in self._wires:
            if wire._wireoutput == inputID:
                return wire._wireinput
        return None

    def _followWireReverse(self, outputID):
        """
        The _followWireReverse function takes an output-ID and follows the wire to the
        next element in the chain to return the ID of the Block-Output connected to it.
        """
        for wire in self._wires:
            if wire._wireinput == outputID:
                return wire._wireoutput
        return None

    def _findObject(self, objectID):
        """
        The function cycles through all elements in the subroutine and looks for
        the corresponding input ID. It returns a reference to the object (its ID)
        and the outgoing IDs.
        """
        for object in self._objects:
            for pin in object._pins:
                if pin["id"] == objectID:
                    outPinList = object.getPinIdByClass("flowobjectoutput")
                    return outPinList, object
        return None, None

    def debugPrint(self):
        print("SUBROUTINE HERE\n" +50 * "=")
        for obj in self._objects:
            print("OBJ", obj._type, "(" + obj._id + ")")
            for pin in obj._pins:
                print(" >", "ID" + pin["id"], pin["pinclass"], pin["name"])
        for wire in self._wires:
            print("WIR", wire._type)
            for point in wire._points:
                print(" |", "ID" + point["id"], "RE" + point["resolve"], point["type"])

    def buildGraph(self):
        '''
        This function builds a multidimensional, partly kind of recursive graph
        to representate the general structure of the main blocks. It partially
        ignores data-wires and its connections so the path is kept very slim
        '''
        for startobject in self._objects:
            if startobject._type in ["ftProProcessStart", "ftProSubroutineFlowIn"]:
                elChain = {"obj": "start", "next": []}
                elementChain = self.__buildGraphRec(startobject)
                self._connectionChains.append(elementChain)
        return self._connectionChains

    def __buildGraphRec(self, startObj):
        '''
        This is a helper function of the buildGraph-function. It fetches all out-
        going objects and adds them to a list so the main function can follow
        those traces.
        '''
        elChain = {"aobj": startObj, "next": []}
        followIdList = startObj.getPinIdByClass("flowobjectoutput")
        followIdList += startObj.getPinIdByClass("dataobjectoutput")
        for beginPin in followIdList:
            endPin = self._followWire(beginPin)
            endObj = self._findObject(endPin)[1]
            if endObj is not None:
                elChain["next"].append(self.__buildGraphRec(endObj))
        return elChain


    def run(self, startObj=None):
        '''
        The run function is mainly called in two situations.
        1) The subroutine is started as an Main-Program. It doesn't have a Sub-
        program-Input-Block but one or more main start-blocks. Each block should
        be run in an own thread, following all elements down the logical structure.
        2) The subroutine is referenced and started by another subprogram. It now
        acts to the outside-function as an roObject, dedicated to do its stuff and
        then just return the outputID and optionally some arguments.
        '''
        for startobject in self._objects:
            if startobject._type == "ftProProcessStart":
                # situation 1
                # TODO: create new thread for the following while-lool/start block
                outputID, arguments = startobject.run(self)
                while outputID is not None:
                    # follow the output-wire
                    nextPin = self._followWire(outputID)
                    nextObj = self._findObject(nextPin)[1]
                    # TODO: check, if object has input-values.
                    # if so, backpropagate to get these values
                    outputID, arguments = nextObj.run(self, inputID=outputID)

            elif startobject._type == "ftProSubroutineFlowIn":
                # situation 2
                pass
            else:
                return None
