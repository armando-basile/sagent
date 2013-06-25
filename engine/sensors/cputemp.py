#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get cpu temperature using sensors command"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.3.0"
__date__       = "2013-06-24"
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
    sensors = os.popen("sensors").read()
    rows = sensors.split('\n')
    
    for row in rows:
        row = row.replace("\r", "")
        
        pos = -1
        try:
            pos = row.index("Core " + str(PARAMS) + ":")
        except:
            pass
        
        if (pos == 0):
            row = row[row.index(":")+1:].strip()
            temp = row[0:row.index(" ")].strip()
            temp = temp.decode('utf-8').replace(u"°C", "")
            outval = round(float(temp), 2)
            
            # debug
            return outval

    return "ERR"

# test method
print GetValue()
