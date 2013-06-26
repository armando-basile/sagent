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
import usb


# use main logger
logger = logging.getLogger("sagent")



# sensor plugin class
class SensorClass():
    
    # product and vendor id
    _VID = 0x0C45
    _PID = 0x7401
    
    # settings
    _REQ_INT_LEN = 8
    _REQ_BULK_LEN = 8
    _TIMEOUT = 2000
    
    # device object
    _device = None
    _handle = None


    # entry point
    def __init__(self, initArgs):
        
        global logger
        
        # use main logger
        self.logger = logger
        
        # get init parameters
        self.params = initArgs
        

    
    
    # get measure from sensor
    def GetValue(self, execArgs):

        # enum all devices to detect Temper Gold
        busses = usb.busses()
        
        for bus in busses:
            for device in bus.devices:
                # check for device
                if ((device.idProduct == self._PID) and (device.idVendor == self._VID)):
                    # device founded
                    self._device = device
        
        
        if (self._device == None):
            self.logger.warning("tempergold::GetValue::error no device founded")
            return "ERR"
        
        try:
            # check for device already opened
            if not self._handle:
                
                # device not opened, try to open
                self._handle = self._device.open()
                
                try:
                    self._handle.detachKernelDriver(0)
                except usb.USBError:
                    pass
                
                try:
                    self._handle.detachKernelDriver(1)
                except usb.USBError:
                    pass
                
                
                self._handle.setConfiguration(1)
                self._handle.claimInterface(0)
                self._handle.claimInterface(1)
                # ini_control_transfer
                self._handle.controlMsg(requestType=0x21, request=0x09, value=0x0201, index=0x00, buffer="\x01\x01", timeout=self._TIMEOUT)
            
            
            self._control_transfer(self._handle, "\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura
            self._interrupt_read(self._handle)
            self._control_transfer(self._handle, "\x01\x82\x77\x01\x00\x00\x00\x00") # uIni1
            self._interrupt_read(self._handle)
            self._control_transfer(self._handle, "\x01\x86\xff\x01\x00\x00\x00\x00") # uIni2
            self._interrupt_read(self._handle)
            self._interrupt_read(self._handle)
            self._control_transfer(self._handle, "\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura
            
            data = self._interrupt_read(self._handle)      
            
            # check for negative value
            b1 = data[2]
            b2 = data[3]
            if (data[2] & 0x80):                 
                b1 = -0x10 + data[2]
            
            tempdata = (b1 << 8) + (b2 & 0xFF)
            temp_c = (125.0/32000.0)*(tempdata)
            return round(temp_c, 2)

        except usb.USBError, e:
            self.logger.error("tempergold::GetValue::error " + e.message)
            self.close()            
            return "ERR"


    def _control_transfer(self, handle, data):
        handle.controlMsg(requestType=0x21, request=0x09, value=0x0200, index=0x01, buffer=data, timeout=self._TIMEOUT)

    
    def _interrupt_read(self, handle):
        return handle.interruptRead(0x82, self._REQ_INT_LEN)



    # try to release interface
    def close(self):
        if self._handle:
            try:
                self._handle.releaseInterface()
            except ValueError:
                pass
            
            self._handle = None


        
        
        
        

# test get measure
#print SensorClass("").GetValue("")
