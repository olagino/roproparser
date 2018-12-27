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


ropro = RoboProProgram("../test/8.1_soundtest.rpp")
ropro.run()
