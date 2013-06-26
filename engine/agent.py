#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Manage measurement readings and notifications for all sensors"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.5.0"
__date__       = "2013-06-26"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"


import socket
import thread
import importlib
import threading
import xml.etree.ElementTree as etree
import datetime
import time
import sys
import atexit
from entity import entity_sensor
import dbmanager
from daemon import runner
import logging
import logging.config


# application path
APPPATH = sys.path[0]
#APPPATH = "/run/media/armando/DEVDRIVE/sviluppo/python/sagent_engine"

# collection of entity_sensor
es = []







# class to manage web app requests
class SocketServerClass():
    
    isRunning = True
    port = 9800
    
    # entry point
    def __init__(self):
        # on exit recall function terminate
        atexit.register(self.OnTerminate)
        
    
    
    # Socket Server
    def RunSocketServer(self, sport):
        global logger

        client = None
        host = ''
        self.port = int(sport)
        backlog = 10
        self.isRunning = True
        
        time.sleep(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:        
            
            s.bind((host,self.port))
            s.listen(backlog)
            logger.info("Sagent Socket Server started")
            
        except Exception, le:
            # error detected
            logger.error("RunSocketServer::listen start error " + str(le.args))
            return
            
        # process requests until service is up
        while (self.isRunning == True):
            time.sleep(0.01)

            # accept request
            client, address = (None, None)
            try:
                client, address = s.accept()
                time.sleep(0.01)
                
            except Exception, e:
                # error detected
                logger.error("RunSocketServer::error " + str(e.args))
                
            
            # check for 
            if (self.isRunning == False):
                break
            
            if (client):
                # manage client
                thread.start_new_thread(self.ProcessClient, (client,))


        # close connection and socket
        if (client):
            client.close()
        s.close()
    
            

            
    
    
    
    # Manage web app client handler
    def ProcessClient(self, reqClient):
        global logger
        size = 1024
        
        try:            
            # get request data
            data = reqClient.recv(size)
            
            # if there is data, parse it
            if data:                        
                reqClient.send(self.ProcessRequest(data))

            # after close connection
            reqClient.close() 
        
        except Exception, e:
            # error detected
            logger.error("ProcessClient::error " + str(e.args))



    
    
    # Elab request arrived 
    def ProcessRequest(self, reqData):
        global APPPATH
        global es
        global logger
        
        # remove CrLf and set response as request
        reqData = reqData.replace('\r', '').replace('\n', '')
        resp = reqData
        
        # check for sensor list request
        if (reqData == "LIST"):
            # request of sensor list arrived
            resp = ""
            for sensor in es:                                
                # update response with sensor data informations
                resp += sensor.NAME + "|" + str(sensor.MIN) + "|" + str(sensor.MAX) + "$"
            
            # return list
            return resp
        
        
        try:
            # check for sensor in enabled sensors collection
            for sensor in es:                
                if (sensor.NAME == reqData):
                    # sensor founded, try to tetrieve measure
                    resp = str(sensor.SENSORCLASS.GetValue(sensor.PARAMS))
                    
        except Exception, e:
            logger.error("ProcessRequest::req: " + reqData + " - error " + e.message)
        
        return resp + "\r\n"




    # recall on terminate is invoked    
    def OnTerminate(self):
        global logger

        self.isRunning = False
        time.sleep(2)














# manage monitor of sensors
class agent():

    # BEGIN CONFIG PARAMETERS ****************************************        
    PIDFILEPATH = "/var/run/sagent.pid"
    LOGFILEPATH = "/var/tmp/sagent.log"
    PIDTIMEOUT = 3    
    DBFILEPATH = "/var/tmp/sagent.sqlite"
    SPORT = 9800
    # END CONFIG PARAMETERS ******************************************


    
    # engine that monitor sensors
    def run(self):
        global logger
        global es
        
        # running Socket Server thread
        ssc = SocketServerClass()
        t = threading.Thread(target=ssc.RunSocketServer, args=(self.SPORT,))
        t.daemon = True
        t.start()

        # init dbfile connection
        dbmanager.DBOpen(self.DBFILEPATH)
        
        
        while True:
            try:
                
                time.sleep(0.5)
                
                # get actual date and time
                atNow = datetime.datetime.now()
                
                # loop for each sensor
                for sensor in es:
                    
                    # check for sensor monitor is enabled
                    if sensor.ENABLED == 1:

                        # check for valid latest check
                        if (sensor.LASTCHECK != ""):
                            limitDateTime = (sensor.LASTCHECK + datetime.timedelta(0, sensor.REFRESH))
                            
                            # check for time to refresh measure
                            if (atNow > limitDateTime):                                
                                # refresh requested                    
                                sensor.LASTCHECK = atNow
                                # process measure (update db, verify to send notify)                    
                                self.UpdateMeasures(sensor)
                                
                        
                        else:
                            # empty date time, refresh requested                
                            sensor.LASTCHECK = atNow
                            # process measure (update db, verify to send notify)                
                            self.UpdateMeasures(sensor)
                
            except Exception, e:
                # error detected
                logger.error("agent::run::error " + e.message)
        
        
        
        
    
    
    # Update measures database and manage out of range value
    def UpdateMeasures(self, sObj):
        global APPPATH
        global logger
        

        # execute script to detect measure
        retValue = str(sObj.SENSORCLASS.GetValue(sObj.PARAMS))
        
        if retValue == "ERR":
            # error detected, manage it...
            logger.error(sObj.NAME + " error")
            return
        
        # update measures in database
        dbmanager.DBInsert(sObj.NAME, retValue)
        
        # check for out of range
        if ((float(retValue) < float(sObj.MIN)) or \
            (float(retValue) > float(sObj.MAX))):
            
            logger.warning("out of range measure...")
            
            # check for configured notifier
            if (sObj.NOTIFIER != ""):
                
                # Send notify using configured notifier plugin
                sObj.NOTIFIERCLASS.SendNotify(sObj.NPARAMS)
                


    

    
    # read xml config file to update sensors structure
    def ReadSensorsConfigFile(self):
        global APPPATH
        global es
        
        # parse xml config file
        tree = etree.parse(APPPATH + "/sensors/sensors.xml") # GET XML SENSORS DESCRIPTOR
        rootNode = tree.getroot()
        sensorNodes = rootNode.findall("./sensor")
        
        # update sensors structure
        for sensorNode in sensorNodes:
            tmp = entity_sensor()
            tmp.NAME = sensorNode.get("name")
            tmp.ENABLED = int(sensorNode.find("./enabled").get("value"))
            tmp.MIN = float(sensorNode.find("./min").get("value"))
            tmp.MAX = float(sensorNode.find("./max").get("value"))
            tmp.REFRESH = float(sensorNode.find("./refresh").get("value"))
            tmp.SCRIPT = sensorNode.find("./script").get("value")
            tmp.IPARAMS = sensorNode.find("./iparams").get("value")
            tmp.PARAMS = sensorNode.find("./params").get("value")
            tmp.NOTIFIER = sensorNode.find("./notifier").get("value")
            tmp.NIPARAMS = sensorNode.find("./niparams").get("value")
            tmp.NPARAMS = sensorNode.find("./nparams").get("value")
            tmp.LASTCHECK = ""
            
            # create instance of sensor plugin class
            mod = importlib.import_module("sensors." + tmp.SCRIPT)        
            tmp.SENSORCLASS = mod.SensorClass(tmp.IPARAMS)
            
            # check for configured notifier plugin
            if tmp.NOTIFIER != "":
                # create instance of notifier plugin class
                mod = importlib.import_module("notifiers." + tmp.NOTIFIER)
                tmp.NOTIFIERCLASS = mod.NotifierClass(tmp.NIPARAMS)
            
            es.append(tmp)

    
    # read settings xml config file
    def ReadSettingsConfigFile(self):
        global APPPATH
        
        # parse xml config file
        tree = etree.parse(APPPATH + "/sagent-settings.xml")
        rootNode = tree.getroot()
        
        settingsNode = rootNode.findall("./settings")

        self.SPORT = settingsNode[0].find("./serverport").get("value")
        self.DBFILEPATH = settingsNode[0].find("./dbfilepath").get("value")
        self.LOGFILEPATH = settingsNode[0].find("./logfilepath").get("value")
        self.PIDFILEPATH = settingsNode[0].find("./pidfilepath").get("value")





    # entry point
    def __init__(self):
        global APPPATH
        
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  self.PIDFILEPATH
        self.pidfile_timeout = self.PIDTIMEOUT
        
        # read xml config file for settings
        self.ReadSettingsConfigFile()
        
        # read xml config file for sensors
        self.ReadSensorsConfigFile()
        




# setup logging object and write message
logger = logging.getLogger("sagent")
logger.setLevel(logging.INFO)

# file handler
formatter1 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - P:%(process)d - %(module)s : %(lineno)d - %(message)s")
handler1 = logging.FileHandler(agent.LOGFILEPATH)
handler1.setFormatter(formatter1)
logger.addHandler(handler1)

# console handler
#formatter2 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler2 = logging.StreamHandler(sys.stdout)
#handler2.setFormatter(formatter2)
#logger.addHandler(handler2)




logger.warning("request service " + sys.argv[1])
    
# Manage daemon action
app = agent()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.daemon_context.files_preserve = [handler1.stream]
daemon_runner.do_action()

logger.info("Sagent Socket Server stopped")















