#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get cpu temperature using sensors command"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["..."]
__license__    = "GPL"
__version__    = "0.1.5.0"
__date__       = "2013-06-26"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"



import os
import logging


# use main logger
logger = logging.getLogger("sagent")


# sensor plugin class
class SensorClass():
    
    
    
    # entry point
    def __init__(self, initArgs):
        
        global logger
        
        # use main logger
        self.logger = logger
        
        # get init parameters
        self.params = initArgs



    
    
    
    # get measure from sensor
    def GetValue(self, execArgs):
        
        # using sensors command
        sensors = os.popen("sensors").read()
        rows = sensors.split('\n')
        
        # parse command output
        for row in rows:
            row = row.replace("\r", "")
            
            pos = -1
            try:
                # try to find temperature information
                pos = row.index("Core " + str(self.params) + ":")
            except:
                pass
            
            # check for temperature information presence
            if (pos == 0):
                #remove unused chars
                row = row[row.index(":")+1:].strip()
                temp = row[0:row.index(" ")].strip()
                temp = temp.decode('utf-8').replace(u"°C", "")
                
                outval = round(float(temp), 2)
                
                # debug
                return outval

        return "ERR"



# test get measure
#print SensorClass("1").GetValue("")
