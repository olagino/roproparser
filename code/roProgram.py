#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup
from roSubroutine import RoboProSubroutine
from roIOWrap import RoboProIOWrap

__author__     = "Leon Schnieber"
__copyright__  = "Copyright 2018"
__credits__    = "fischertechnik GmbH"
__maintainer__ = "Leon Schnieber"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"


class RoboProProgram(object):
    """
    The RoboProProgram-Class is able to parse and execute a .rpp-File generated
    from the RoboPro-Software.
    """


    def __init__(self, xmlstr):
        self.soup = BeautifulSoup(xmlstr, "xml")
        self._subroutines = {}
        self._io = RoboProIOWrap()
        self.parse()

    def parse(self):
        """
        Parsing the XML-Structure for Subroutines. For each found subroutine a
        new instance of the Subroutine-Class is initialized.
        """
        subroutinesRaw = self.soup.find_all("o", attrs={
            "classname": "ftProSubroutineFunction"})
        for subRaw in subroutinesRaw:
            self.addNewSubroutine(subRaw)

    def addNewSubroutine(self, subRaw):
        subRtName = subRaw.attrs["name"]
        subRtObj = RoboProSubroutine(subRaw)
        subRtObj._subrts = self._subroutines
        subRtObj.setIO(self._io)
        self._subroutines[subRtName] = subRtObj

    def run(self, subroutine="Hauptprogramm"):
        if subroutine in self._subroutines:
            subObj = self._subroutines[subroutine]
            subObj.run()
