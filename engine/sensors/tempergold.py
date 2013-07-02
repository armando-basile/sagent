#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Get temperature using Temper Gold usb sensor 0x0C45:0x7401"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["..."]
__license__    = "GPL"
__version__    = "0.1.5.1"
__date__       = "2013-07-02"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"

"""
Changelog:
    0.1.5.0
        - first release
    
    0.1.5.1
        - fix: measured zero value at each start


"""

import threading
import atexit
import logging
import logging.config
import usb
import time
#import sys


# sensor plugin class
class SensorClass():
    
    
    # device static attributes
    temperGoldValue = [None]
    temperGoldState = [0]
    
    

    # entry point
    def __init__(self, initArgs):
        # on exit recall function terminate
        atexit.register(self.OnTerminate)
        
        # usb objects        
        self._temperGoldHandle = None
        self._temperGoldDevice = None
        
        # product and vendor id
        self._VID = 0x0C45
        self._PID = 0x7401
        
        # settings
        self._REQ_INT_LEN = 8
        self._REQ_BULK_LEN = 8
        self._TIMEOUT = 2000
        
        # use main logger
        self.logger = logging.getLogger("sagent")
        # DEBUG ONLY
        #logger.setLevel(logging.INFO)
        # file handler
        #formatter1 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - P:%(process)d - %(module)s : %(lineno)d - %(message)s")
        #handler1 = logging.StreamHandler(sys.stdout)
        #handler1.setFormatter(formatter1)
        #logger.addHandler(handler1)
        
        # attach static objects to manage multithread
        self._temperGoldValue = SensorClass.temperGoldValue
        self._temperGoldState = SensorClass.temperGoldState
        
        # get init parameters
        self.params = initArgs
        

    # recall on terminate is invoked    
    def OnTerminate(self):

        self._temperGoldState[0] = 5        
        time.sleep(2)

    
    # init after instance created
    def Init(self):
        if self._temperGoldState[0] != 0:
            self.logger.info("tempergold::Init:: already called")
            return
        
        # laungh measure reader      
        rT = threading.Thread(target=self.StartReading, args=())
        rT.daemon = True
        rT.start()
        return
    
    
    # close engine
    def Close(self):
        self._temperGoldState[0] = 3
        


    
    # get measure from sensor
    def GetValue(self, execArgs):
        
        # check for device working
        if self._temperGoldState[0] != 2:
            self.logger.info("tempergold::GetValue:: device not ready [" + str(self._temperGoldState[0]) + "]")
            return "ERR"
        
        if self._temperGoldValue[0]:
            # return latest readed measure
            return self._temperGoldValue[0]
            
        else:
            # first value not yet readed
            return "ERR"
        




    def control_transfer(self, data):
        try:
            self._temperGoldHandle.controlMsg(requestType=0x21, request=0x09, value=0x0200, index=0x01, buffer=data, timeout=self._TIMEOUT)
        except Exception, e:
            self.logger.error("tempergold::_control_transfer::error " + str(e))
            raise e

    
    def interrupt_read(self):
        try:
            return self._temperGoldHandle.interruptRead(0x82, self._REQ_INT_LEN)
        except Exception, e:
            self.logger.error("tempergold::_interrupt_read::error " + str(e))
            raise e


    # try to release interface and device
    def close(self):
        if self._temperGoldHandle:
            try:
                self._temperGoldHandle.releaseInterface()
            except ValueError:
                pass
            
            self._temperGoldHandle = None



    # engine to read measure from device
    def StartReading(self):
        
        # check for device state
        if self._temperGoldState[0] != 0:
            self.logger.info("tempergold::StartReading:: already called [" + str(self._temperGoldState[0]) + "]")
            return
        
        self._temperGoldState[0] = 1
        self.logger.info("tempergold::StartReading:: called")
        
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
            self.logger.error("tempergold::StartReading::error " + e.message)
            return
        
        # check for device presence
        if not self._temperGoldDevice:
            self.logger.error("tempergold::StartReading::error no device founded")
            return
        
        self.logger.info("tempergold::StartReading:: device founded, start reading")
        self._temperGoldState[0] = 2
        
        while self._temperGoldState[0] == 2:
            
            try:
                time.sleep(5)                
                # if first time init handle
                if not self._temperGoldHandle:
                    # try to open
                    self.logger.info("tempergold::StartReading:: device opening")
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
                
                # exchange to get measure
                self.control_transfer("\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura
                self.interrupt_read()
                self.control_transfer("\x01\x82\x77\x01\x00\x00\x00\x00") # uIni1
                self.interrupt_read()
                self.control_transfer("\x01\x86\xff\x01\x00\x00\x00\x00") # uIni2
                self.interrupt_read()
                self.interrupt_read()
                self.control_transfer("\x01\x80\x33\x01\x00\x00\x00\x00") # uTemperatura
    
                data = self.interrupt_read()
                
                # check for negative value
                b1 = data[2]
                b2 = data[3]
                if (data[2] & 0x80):                 
                    b1 = -0x10 + data[2]
                
                tempdata = (b1 << 8) + (b2 & 0xFF)
                temp_c = (125.0/32000.0)*(tempdata)
                self._temperGoldValue[0] = round(temp_c, 2)
                

                # close handle
                #self.close()

    
            except usb.USBError, e:            
                self.logger.error("tempergold::StartReading::error " + e.message)
                #self.close()                
                
        self.logger.info("tempergold::StartReading:: closing")
        self.close()


































