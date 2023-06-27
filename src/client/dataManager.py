#-----------------------------------------------------------------------------
# Name:        dataManage.py
#
# Purpose:     Data manager class used to provide specific data fetch and process 
#              functions and init the local data storage/DB. This manager is used 
#              by the scheduler(<actionScheduler>) obj.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2
# Created:     2023/01/11
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import json

from datetime import datetime

import probeGlobal as gv
import Log

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(object):
    """ The data manager is a module running parallel with the main thread to 
        handle the data-IO with dataBase and the monitor hub's data fetching/
        changing request.
    """
    def __init__(self, parent, fetchMode=True) -> None:
        self.parent = parent
        self.terminate = False
        self.fetchMode = fetchMode
        self.reportInterval = 0
        self.lastUpdate = datetime.now()
        self.resultDict = {}
    
    #-----------------------------------------------------------------------------
    def archiveResult(self, resultDict):
        self.resultDict = resultDict
        gv.gDebugPrint(json.dumps(resultDict), prt=False, logType=gv.LOG_INFO)
        return None
    
    #-----------------------------------------------------------------------------
    def getResultDict(self):
        return self.resultDict
