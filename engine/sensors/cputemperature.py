#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get cpu temperature using acpi or sys/devices file"
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

# Read method
def GetValue():
    global PARAMS
    global logger
    
    temp = ""
    if os.path.exists("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp") == True:
        temp = open("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp").read().strip()
        temp = str(float(temp)/1000)
    
    elif os.path.exists("/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp") == True:
        temp = open("/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp").read().strip()
        temp = str(float(temp)/1000)
        
    elif os.path.exists("/proc/acpi/thermal_zone/THM0/temperature") == True:
        temp = open("/proc/acpi/thermal_zone/THM0/temperature").read().strip()
    
    elif os.path.exists("/proc/acpi/thermal_zone/THRM/temperature") == True:
        temp = open("/proc/acpi/thermal_zone/THRM/temperature").read().strip()

    elif os.path.exists("/proc/acpi/thermal_zone/THR1/temperature") == True:
        temp = open("/proc/acpi/thermal_zone/THR1/temperature").read().strip()

    else:
        temp = "ERR"

    return temp





print GetValue()

