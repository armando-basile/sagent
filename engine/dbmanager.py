#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__        = "Manage sqlite database to store surveys"
__author__     = "Armando Basile"
__copyright__  = "copytight (c) 2013"
__credits__    = ["AUTHOR_NAME"]
__license__    = "GPL"
__version__    = "0.1.2.0"
__date__       = "2013-06-21"
__maintainer__ = "Armando Basile"
__email__      = "armando@integrazioneweb.com"
__status__     = "Stable"



import sqlite3 as lite
import sys
import datetime
import logging

con = None

logger = logging.getLogger("sagent")

# sql command to create db table
sqlCreateTable = "CREATE TABLE IF NOT EXISTS surveys (" + \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, " + \
                    "date_time string NOT NULL, " + \
                    "paramid string NOT NULL, " + \
                    "paramvalue string NOT NULL " + \
                    "); "

# sql command to create db indexes
sqlCreateIndexes = ["CREATE INDEX IF NOT EXISTS idx_surveys_date_time ON surveys (date_time ASC); ",
                    "CREATE INDEX IF NOT EXISTS idx_surveys_paramid ON surveys (paramid ASC); ",
                    "CREATE INDEX IF NOT EXISTS idx_surveys_paramvalue ON surveys (paramvalue ASC); ", ]


# open or create measures database
def DBOpen(dbPath):
    global con
    global sqlCreateTable
    global sqlCreateIndexes
    global logger
    
    try:
        # try to open/create
        con = lite.connect(dbPath)
        con.execute("pragma foreign_keys=on;")
        con.execute("pragma synchronous=off;")
        con.execute("pragma journal_mode=memory;")
        con.execute(sqlCreateTable)
        con.execute(sqlCreateIndexes[0])
        con.execute(sqlCreateIndexes[1])
        con.execute(sqlCreateIndexes[2])

    
    except lite.Error, e:
        # error detected
        logger.error("DBOpen(" + dbPath + ") Error " + e.args[0])        
        sys.exit(11)




# insert measure in database
def DBInsert(pId, pValue):
    global con
    global logger
    
    datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cmdSql = "INSERT INTO surveys (date_time, paramid, paramvalue) " + \
             "VALUES ('" + datenow + "', '" + pId + "', '" + pValue + "')"
    
    try:
        con.execute(cmdSql)
        con.commit()
    
    except lite.Error, e:
        # error detected
        logger.error("INSERT " + cmdSql + "\r\nError " + e.args[0])
        sys.exit(12)


# close connection if exists
def DBClose():
    global con
    if (con):
        con.close()





















