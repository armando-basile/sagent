#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Entity to manage sensor data"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.2.0"
__date__       = "2013-06-21"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"


class entity_sensor():
    ENABLED = ""
    NAME = ""
    MIN = 0
    MAX = 0
    REFRESH = 60
    SCRIPT = ""
    PARAMS = ""
    LASTCHECK = ""
    NOTIFIER = ""
    NPARAMS = ""
    
