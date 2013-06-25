#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Send sms to notify out of range value of an active sensor"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.0.0"
__date__       = "2013-06-24"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"


import smsgateway
import sys
import logging

logger = logging.getLogger("sagent")

# set parameters
PARAMS=sys.argv[1]

def SendNotify():
    global PARAMS
    global logger
    
    indata = PARAMS.split('|')
    
    
    # create sms gateway instance and init class
    phone = smsgateway.Sms()
    ret = phone.Init()

    # check for successful init    
    if (ret != ""):
        # error detected
        logger.error("sms::SendNotify::Init error " + ret)
        return
    
    ret = phone.Send(indata[0], indata[1])
    # check for successful send
    if (ret != ""):
        # error detected
        logger.error("sms::SendNotify::Send error " + ret)
        return

    return


# method to send notify
SendNotify()
