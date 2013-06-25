#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Using sensors command with grep parameter"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.2.0"
__date__       = "2013-06-21"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"


import os
import sys
import logging

logger = logging.getLogger("sagent")

# set core id to check
PARAMS=sys.argv[1]

def GetValue():
    global PARAMS
    global logger
    sensors = os.popen("sensors | grep \"Core" + str(PARAMS) + " Temp\"").read()
    rows = sensors.split('\n')
    if len(rows) > 0:
        pos = rows[0].index(":")
        row = rows[0][pos+1:].strip().replace("°C", "")
        outval = round(float(row), 2)
        
        # ret value
        return outval

    return "ERR"

# test method
print GetValue()
