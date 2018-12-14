#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup
from roProgram import RoboProProgram
import time

__author__     = "Leon Schnieber"
__copyright__  = "Copyright 2018"
__credits__    = "fischertechnik GmbH"
__maintainer__ = "Leon Schnieber"
__email__      = "olaginos-buero@outlook.de"
__status__     = "Developement"


file = open("../test/8.4_basic.rpp", "r")
# file = open("../test/testprogramm.rpp", "r")
text = "".join(file.readlines())
ropro = RoboProProgram(text)
# ropro._subroutines["Hauptprogramm"].debugPrint()
# print(ropro._subroutines["up1"]._subroutineRaw)
ropro.run()

# file = open("../test/input_test.rpp", "r")
# text = "".join(file.readlines())
# ropro = RoboProProgram(text)
# subrout = ropro._subroutines["Hauptprogramm"]
# for obj in subrout._objects:
#     if obj._type == "ftProDataMssg":
#         print("OBJ", obj._type, "(" + obj._id + ")")
#         data = obj._objectRaw.attrs["command"]
#         print(data)
#     else:
#         print(obj._type)
