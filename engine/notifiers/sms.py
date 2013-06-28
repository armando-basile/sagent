#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Send sms to notify out of range value of an active sensor"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.5.0"
__date__       = "2013-06-26"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"


"""
HOW TO USE THIS PLUGINS

you need to config plugin parameter (niparams) using sensor node parameters in
sagent xml config file sensors/sensors.xml. 

xxx,yyy where xxx=serial port device and yyy=sms center phone number

"""

import threading
import smsgateway
import logging
import Queue
import time


# notifier plugin class
class NotifierClass():

    # create static flag to manage device usage
    InitStatus = 0

    # create static queue
    Messages = Queue.Queue()

    # create static gsm device manager
    Phone = smsgateway.Sms()
    
    # main logger
    logger = logging.getLogger("sagent")
    

    # entry point
    def __init__(self, initArgs):
        
        # flag to check ready state
        self._isReady = False

        # check for init already called
        if (NotifierClass.InitStatus != 0):
            return
        
        # set init started
        NotifierClass.InitStatus = 1

        # extract arguments from parameter
        args = initArgs.split(',')
        
        if (len(args) != 2):
            NotifierClass.logger.error("sms::Init::error parameters <> 2, check sensors.xml settings")
            return
        
        # create sms gateway instance and init class        
        ret = NotifierClass.Phone.Init(args[0], args[1])

        # check for successful init    
        if (ret != ""):
            # error detected
            NotifierClass.logger.error("sms::Init::error " + ret)
            return
        
        # run message queue checker
        mt = threading.Thread(target=NotifierClass._MessageChecker)
        mt.daemon = True
        mt.start()
                
        self._isReady = True
        
        


    
    # Send notify
    def SendNotify(self, execArgs):
        
        # check for ready status
        if (self._isReady != True):
            NotifierClass.logger.error("sms::SendNotify::error sms notifier isn't ready")
            return
        
        # add message to queue
        NotifierClass.Messages.put(execArgs)
        
        return



    # manage send of sms
    def _SendMessage(msgToSend):
        
        indata = msgToSend.split('|')
        
        # Send data parameters:
        # first = message to send
        # second = phone nomber
        
        ret = NotifierClass.Phone.Send( indata[0], indata[1])
        # check for successful send
        if (ret != ""):
            # error detected
            NotifierClass.logger.error("sms::_SendMessage::error " + ret)
            return
    
        return
        


    # Thread to scan messages queue
    def _MessageChecker():
        
        while (True):
            
            # check for message in queue
            if (NotifierClass.Messages.empty() == False):
                
                # check all messages
                while (NotifierClass.Messages.empty() == False):
                    
                    # get and send message
                    msg = NotifierClass.Messages.get()
                    NotifierClass._SendMessage(msg)
                    
                    # wait for some seconds
                    time.sleep(3)
            
            # wait for 1 minute between scan
            time.sleep(60)








