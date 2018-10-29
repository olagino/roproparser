#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup

__author__     = "Leon Schnieber"
__copyright__  = "Copyright 2018"
__credits__    = "fischertechnik GmbH"
__maintainer__ = "Leon Schnieber"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"


class RoboProWire(object):
    """
    This object is generated by an XML-String or via the attributes
    itself. Therefor objectXmlSoup has to be None so the attributes can be set
    manually. This feature is mainly used for Pseudo-Objects used on converging
    wires.
    """
    def __init__(self, wireXmlSoup=None):
        self._wireRaw = wireXmlSoup
        self._type = ""
        self._points = []
        self._wireinput = ""
        self._wireoutput = ""
        if self._wireRaw is not None:
            self.parse()

    def parse(self):
        self._type = self._wireRaw.attrs["classname"]
        pinList = self._wireRaw.find_all("o", attrs={
            "classname": "wxCanvasPin"
        })
        for pin in pinList:
            pinData = {
                "id": pin.attrs["id"],
                "name": pin.attrs["name"],
                "resolve": pin.attrs["resolveid"],
                "type": pin.attrs["pinclass"]
            }
            self._points.append(pinData)
            if "wireoutput" in pinData["type"]:
                self._wireoutput = pinData["resolve"]
            elif "wireinput" in pinData["type"]:
                self._wireinput = pinData["resolve"]

    def getObjectWireList(self):
        """
        dynamic:
        - create object with dynamic-id as outpin, resolveid as inpin
        - create wire (end = dynamic-id, begin = orig-begin)
        """
        wireList = []
        objectList = []
        category = "flow" if "flow" in self._type else "data"
        linkto = ""
        for point in self._points:
            if "wireinput" in point["type"]:
                linkto = point["resolve"]
            elif point["name"] == "dynamic":
                wire = {
                    "wireinput": linkto,
                    "wireoutput": point["id"],
                    "type": self._type
                }
                wireList.append(wire)
                object = {
                    "type": category + "Helper",
                    "pin": [
                        {
                            "type": category + "objectinput",
                            "id": point["id"]
                        },
                        {
                            "type": category + "objectoutput",
                            "id": point["id"]
                        }
                    ]
                }
                objectList.append(object)
        return wireList, objectList
