#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import serial


class Sms:
    
    # Sms class constructor
    def __init__(self):
        
        # timing
        self.__waitrw         = 0.3                  # seconds between sends    
        self.__readtout       = 3                    # read timeout in seconds
        self.__comport        = "/dev/ttyACM0"       # com port to exchange data with phone
        self.__baudrate       = 9600                 # serial speed    
        self.__readBuff       = 1024                 # read buffer size
        self.__smscenter      = "+393916263900"      # FASTWEB SMS Center
                
        # object to manage phone/sim card communication
        self.__phone = None
        
    
    
    # read data from serial port
    def ReadData(self, readTimeOut):        
        
        endtime = datetime.datetime.now() + datetime.timedelta(0, readTimeOut)
        actual = datetime.datetime.now()
        tmpmsg = ""        
        
        while (actual < endtime):
            
            toRead = self.__phone.inWaiting()
            
            # try to read on serial port
            if toRead > 0:
                tmpmsg = self.__phone.read(toRead)
                break

            # update actual time
            actual = datetime.datetime.now()

            
        # if buffer is empty, exit
        if len(tmpmsg) == 0:
            return ""
        
        # append to output message
        outmsg = tmpmsg
        
        # if there are bytes to read, read it
        while self.__phone.inWaiting() > 0:
            
            # try to read on serial port
            tmpmsg = self.__phone.read(self.__readBuff)
            outmsg += tmpmsg
        
        # return readed bytes
        return outmsg
        
    
    
    
    # init phone communication
    def Init(self, comPort, smsCenter):
        
        self.__comport = comPort
        self.__smscenter = smsCenter
        
        # open communication
        self.__phone = serial.Serial(self.__comport, self.__baudrate, timeout=self.__readtout)
        
        try:
            time.sleep(self.__waitrw)
            
            # send ack
            self.__phone.write(b'AT\r')            
            datain = self.ReadData(self.__readtout)
            if datain[-4:] != "OK\r\n":
                return "init error: " + datain
            
            # send sms center
            self.__phone.write(b'AT+CSCA="' + self.__smscenter + '"\r')
            datain = self.ReadData(self.__readtout)
            if datain[-4:] != "OK\r\n":
                return "init error: sms center error: " + datain
            
            # delete all sms received
            #self.__phone.write(b'AT+CMGD=ALL\r')
            #datain = self.ReadData(20)
            #if datain[-4:] != "OK\r\n":
            #    return "init error: all sms deleted error: " + datain
            
            
            
            
        except Exception as e:
            # error detected
            return "init error: [exception] " + e.message

        # return empty 
        return ""





    # send message
    def Send(self, nmessage, number):

        # update message to send
        smsmsg = nmessage.encode() + b"\r"
        
        try:
          
            # check for message len
            if len(smsmsg) > 120:
                return "send error: message is too long"
            
            # send ack
            self.__phone.write(b'AT\r')
            datain = self.ReadData(self.__readtout)
            if datain[-4:] != "OK\r\n":
                return "send error: [1] " + datain
          
            # set communication for text messages
            self.__phone.write(b'AT+CMGF=1\r')
            datain = self.ReadData(self.__readtout)
            if datain[-4:] != "OK\r\n":
                return "send error: [2] " + datain

            # set phone number
            self.__phone.write(b'AT+CMGS="' + number.encode() + b'"\r')            
            datain = self.ReadData(self.__readtout)
            if datain[-2:] != "> ":
                return "send error: [3] " + datain
            
            # set text messages
            self.__phone.write(smsmsg)            
            datain = self.ReadData(self.__waitrw)
            self.__phone.write(chr(26))            
            time.sleep(3)
            datain += self.ReadData(self.__readtout)
            
            if datain[-4:] != "OK\r\n":
                return "send error: [4] " + datain + " [" + datain.encode("hex") + "]"
            
            
        except Exception as e:
            # error detected
            return "send error: [exception] " + e.message


        # return empty if all ok
        return ""
        
        















