#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get cpu temperature using vcgencmd command for raspberry pi"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["..."]
__license__    = "GPL"
__version__    = "0.1.0.0"
__date__       = "2013-07-03"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"



import os
import logging



# sensor plugin class
class SensorClass():
    
    
    
    # entry point
    def __init__(self, initArgs):
        
        # use main logger
        self.logger = logging.getLogger("sagent")
        
        # get init parameters
        self.params = initArgs



    # init after instance created
    def Init(self):
        return
    


    # close engine
    #def Close(self):
    #    # nothing
        
        
    
    # get measure from sensor
    def GetValue(self, execArgs):
        
        # using sensors command
        sensors = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        rows = sensors.split('\n')
        
        # parse command output
        for row in rows:
            row = row.replace("\r", "")
            
            pos = -1
            try:
                # try to find temperature information
                pos = row.index("temp=")
            except:
                pass
            
            # check for temperature information presence
            if (pos == 0):
                #remove unused chars
                temp = row.replace("temp=", "").replace("'C", "").replace(",", ".")
                outval = round(float(temp), 2)
                
                # debug
                return outval

        return "ERR"



# test get measure
#print SensorClass("1").GetValue("")
