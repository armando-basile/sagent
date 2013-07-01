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
import atexit
import smsgateway
import logging
import Queue
import time


# notifier plugin class
class NotifierClass():

    # create static flag to manage device usage
    InitStatus = [0]

    # create static queue
    Messages = Queue.Queue()
        
    # set ready status of device
    IsReady = [False]
    
    
    
    # entry point
    def __init__(self, initArgs):
        
        atexit.register(self.OnTerminate)
        
        # attach static objects to manage multithread
        self._InitStatus = NotifierClass.InitStatus
        self._Messages = NotifierClass.Messages
        self._Phone = None
        self._isReady = NotifierClass.IsReady
        self._iparams = initArgs
        
        # main logger
        self.logger = logging.getLogger("sagent")
        
        
        
    # init after instance created
    def Init(self):
        
        # check for main instance presence
        if self._InitStatus[0] != 0:
            self.logger.info("sms:Init already called")
            return
        
        # trace init request passed
        self.logger.info("sms::Init called")
        
        
        # set init started
        self._InitStatus[0] = 1
        
        # extract arguments from parameter
        args = self._iparams.split(',')
        
        if (len(args) != 2):
            self.logger.error("sms::Init::error parameters <> 2, check sensors.xml settings")
            return
        
        # create sms gateway instance and init class
        self._Phone = smsgateway.Sms()
        ret = self._Phone.Init(args[0], args[1])

        # check for successful init    
        if (ret != ""):
            # error detected
            self.logger.error("sms::Init::error " + ret)
            return
        
        # set initialized done 
        self._InitStatus[0] = 2
        
        # run message queue checker
        mt = threading.Thread(target=self.StartMsgSender, args=())
        mt.daemon = True
        mt.start()





    # recall on terminate is invoked    
    def OnTerminate(self):

        self._InitStatus[0] = 3     
        time.sleep(2)

        

    
    # Send notify
    def SendNotify(self, execArgs):


        # check for ready status
        if (self._InitStatus[0] != 2):
            self.logger.error("sms::SendNotify::error sms notifier isn't ready")
            return
        
        # add message to queue
        self._Messages.put(execArgs)
        
        return





    # manage send of sms
    def _SendMessage(self, msgToSend):
        
        indata = msgToSend.split('|')
        
        # Send data parameters:
        # first = phone nomber
        # second = message to send
        
        
        ret = self._Phone.Send( indata[0], indata[1])
        # check for successful send
        if (ret != ""):
            # error detected
            self.logger.error("sms::_SendMessage::error " + ret)
            return
    
        return
        


    # Thread to scan messages queue
    def StartMsgSender(self):

        # check for main instance presence
        if self._InitStatus[0] != 2:
            self.logger.info("sms:StartMsgSender already called")
            return

        self.logger.info("sms:StartMsgSender called")
        while self._InitStatus[0] == 2:
            
            # check for message in queue            
            if (self._Messages.empty() == False):
                
                # check all messages
                while (self._Messages.empty() == False):
                    self.logger.info("sms::_MessageChecker:: message in queue")
                    # get and send message
                    msg = self._Messages.get()
                    self._SendMessage(msg)
                    self._Messages.task_done()
                    # wait for some seconds
                    time.sleep(2)
            
            # wait for 1 sec
            time.sleep(1)


        self.logger.info("sms::_MessageChecker:: closing")





