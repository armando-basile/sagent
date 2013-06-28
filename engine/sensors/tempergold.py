#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get temperature using Temper Gold usb sensor 0x0C45:0x7401"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["..."]
__license__    = "GPL"
__version__    = "0.1.5.0"
__date__       = "2013-06-26"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"



import logging
import logging.config
import usb
#import sys

# use main logger
logger = logging.getLogger("sagent")

# DEBUG ONLY
#logger.setLevel(logging.INFO)
# file handler
#formatter1 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - P:%(process)d - %(module)s : %(lineno)d - %(message)s")
#handler1 = logging.StreamHandler(sys.stdout)
#handler1.setFormatter(formatter1)
#logger.addHandler(handler1)



# sensor plugin class
class SensorClass():
    
    
    # device static attributes
    temperGoldValue = 0
    temperGoldState = 0


    # entry point
    def __init__(self, initArgs):
        
        global logger
        
        # usb objects
        self._temperGoldDevice = None
        self._temperGoldHandle = None

        # product and vendor id
        self._VID = 0x0C45
        self._PID = 0x7401
        
        # settings
        self._REQ_INT_LEN = 8
        self._REQ_BULK_LEN = 8
        self._TIMEOUT = 2000
        
        # use main logger
        self.logger = logger
        
        # get init parameters
        self.params = initArgs
        


    
    
    # get measure from sensor
    def GetValue(self, execArgs):

        
        # check for device used
        if (SensorClass.temperGoldState == 1):
            return SensorClass.temperGoldValue
        
        # set device in use
        SensorClass.temperGoldState = 1
        
        # enum all devices to detect Temper Gold
        busses = usb.busses()
        
        try:
            for bus in busses:
                for device in bus.devices:
                    # check for device
                    if ((device.idProduct == self._PID) and (device.idVendor == self._VID)):
                        # device founded                    
                        self._temperGoldDevice = device


        except usb.USBError, e:
            self.logger.error("tempergold::GetValue::error " + e.message)
            SensorClass.temperGoldState = 0
            return "ERR"
        
        
        if not self._temperGoldDevice:
            self.logger.error("tempergold::GetValue::error no device founded")
            SensorClass.temperGoldState = 0
            return "ERR"
        

        
        try:

            # try to open
            self._temperGoldHandle = self._temperGoldDevice.open()

            try:
                self._temperGoldHandle.detachKernelDriver(0)
            except usb.USBError:
                pass
            
            try:
                self._temperGoldHandle.detachKernelDriver(1)
            except usb.USBError:
                pass
            
            self._temperGoldHandle.setConfiguration(1)
            self._temperGoldHandle.claimInterface(0)
            self._temperGoldHandle.claimInterface(1)
            # ini_control_transfer
            self._temperGoldHandle.controlMsg(requestType=0x21, \
                request=0x09, value=0x0201, index=0x00, buffer="\x01\x01", \
                timeout=self._TIMEOUT)
            
            self._control_transfer("\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura
            self._interrupt_read()
            self._control_transfer("\x01\x82\x77\x01\x00\x00\x00\x00") # uIni1
            self._interrupt_read()
            self._control_transfer("\x01\x86\xff\x01\x00\x00\x00\x00") # uIni2
            self._interrupt_read()
            self._interrupt_read()
            self._control_transfer("\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura

            data = self._interrupt_read()
            
            # check for negative value
            b1 = data[2]
            b2 = data[3]
            if (data[2] & 0x80):                 
                b1 = -0x10 + data[2]
            
            tempdata = (b1 << 8) + (b2 & 0xFF)
            temp_c = (125.0/32000.0)*(tempdata)
            SensorClass.temperGoldValue = round(temp_c, 2)
            
            self.close()
            # set NON working flag 
            SensorClass.temperGoldState = 0
            
            return round(temp_c, 2)

        except usb.USBError, e:            
            self.logger.error("tempergold::GetValue::error " + e.message)
            # set NON working flag 
            SensorClass.temperGoldState = 0
            self.close()
            return "ERR"



    def _control_transfer(self, data):
        try:
            self._temperGoldHandle.controlMsg(requestType=0x21, request=0x09, value=0x0200, index=0x01, buffer=data, timeout=self._TIMEOUT)
        except Exception, e:
            self.logger.error("tempergold::_control_transfer::error " + str(e))

    
    def _interrupt_read(self):
        try:
            return self._temperGoldHandle.interruptRead(0x82, self._REQ_INT_LEN)
        except Exception, e:
            self.logger.error("tempergold::_interrupt_read::error " + str(e))


    # try to release interface
    def close(self):
        if self._temperGoldHandle:
            try:
                self._temperGoldHandle.releaseInterface()
            except ValueError:
                pass
            
            self._temperGoldHandle = None


        
        
