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


import smsgateway
import logging

logger = logging.getLogger("sagent")


# notifier plugin class
class NotifierClass():


    # entry point
    def __init__(self, initArgs):
        
        global logger
        
        # use main logger
        self.logger = logger
        
        # get init parameters
        self.params = initArgs

        # create sms gateway instance and init class
        self.phone = smsgateway.Sms()
        ret = self.phone.Init()

        # check for successful init    
        if (ret != ""):
            # error detected
            self.logger.error("sms::Init error " + ret)
            return



    
    # Send notify
    def SendNotify(self, execArgs):
        
        indata = execArgs.split('|')
        
        # Send data parameters:
        # first = message to send
        # second = phone nomber
        
        ret = self.phone.Send( indata[0], indata[1])
        # check for successful send
        if (ret != ""):
            # error detected
            self.logger.error("sms::SendNotify::error " + ret)
            return
    
        return



