#-----------------------------------------------------------------------------
# Name:        monitorRun.py
#
# Purpose:     This module is used to collect the data from different agent and 
#              add the data to data base.
#              
# Author:      Yuancheng Liu
#
# Created:     2010/08/26
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import json
from statistics import mean 
from collections import OrderedDict
import monitorServerGlobal as gv
from databaseHandler import  InfluxDB1Cli

import commManager

class monitorRun(object):

    def __init__(self) -> None:
        self.clientIPList = [
            ('127.0.0.1', 3001),
            ('192.168.35.101', 3001),
            ('192.168.35.102', 3001),
            ('192.168.35.103', 3001),
            ('192.168.35.104', 3001),

        ]
        self.commMgr = commManager.commManager()
        self.commMgr.initUDPClient('127.0.0.1', 3001)
        self.dataDict = dict()
        for ipAddr in self.clientIPList:
            key = ipAddr[0]
            self.dataDict[key] = {
                'cpu': 0,
                'ram': 0,
                'ping': 1000,
            }
        self.scoreDBhandler = InfluxDB1Cli(ipAddr=gv.gScoreDBAddr, dbInfo=gv.gScoreDBInfo)
        self.terminate = False

#-----------------------------------------------------------------------------
    def fetchAgentsData(self):
        msg = b'GET;data;{}'
        for ipaddr in self.clientIPList:
            key = ipaddr[0]
            self.dataDict[key] = {
                'cpu': 0,
                'ram': 0,
                'ping': 1000,
            }
            resp = self.commMgr.fetchInfo(ipaddr, msg)
            if resp is None:
                continue
            else:
                k, t, dataStr = resp
                data = json.loads(dataStr)
                self.dataDict[key]['ping'] = self._getPingVal(data)
                self.dataDict[key]['cpu'] = self._getCpuUsage(data)
                self.dataDict[key]['ram'] = self._getRamUsage(data)


    def _getCpuUsage(self, valDict):
        val = valDict['local']['local-1']['result']['cpu']
        return 0 if val is None else  mean(val)
        
    def _getRamUsage(self, valDict):
        val = valDict['local']['local-1']['result']['ram']
        return 0 if val is None else val

    def _getPingVal(self, valDict):
        val = valDict['Internet']['Internet-1']['result']['ping']
        if val is None or len(val) != 3:
             return 1000
        return val[1]


    def _convertToInfluxField(self, dataDict):
        dataFiled = {}
        for key in dataDict:
            data = dataDict[key]
            dataFiled[key+'_cpu'] = float(data['cpu'])
            dataFiled[key+'_ram'] = float(data['ram'])
            dataFiled[key+'_ping'] = float(data['ping'])
        return dataFiled


    def updateDB(self):
        dataFiled = self._convertToInfluxField(self.dataDict)
        self.scoreDBhandler.insertFields(gv.gMeasurement, dataFiled)

    def run(self):
        while not self.terminate:
            print("start to fetch data from clients")
            self.fetchAgentsData()
            print(self.dataDict)
            self.updateDB()
            time.sleep(5)

monitorCli = monitorRun()
monitorCli.run()
