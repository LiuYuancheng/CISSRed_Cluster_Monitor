#-----------------------------------------------------------------------------
# Name:        commManager.py
#
# Purpose:     Communication channel managment module to handle different data/
#              control connection request. The features provided by the module are:
#              - UDP server for data fetch request. 
#              - UDP client for data auto-submission. 
#              - HTTP/HTTPS client for data submittion.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.1
# Created:     2023/03/26
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import time
import json
import requests
import threading

import probeGlobal as gv
import udpCom
import Log

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class udpManager(threading.Thread):
    
    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.udpServer = None
        self.udpClient = None
        self.daemon = True

    def initUDPServer(self, udpPort):
        self.udpServer = udpCom.udpServer(None, udpPort)

    def initUDPClient(self, ipAddr, udpPort):
        self.udpClient = udpCom.udpClient((ipAddr, udpPort))

    #-----------------------------------------------------------------------------
    def _parseIncomeMsg(self, msg):
        """ parse the income message to tuple with 3 elements: request key, type and jsonString
            Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
        """
        req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
        try:
            reqKey, reqType, reqJsonStr = req.split(';', 2)
            return (reqKey.strip(), reqType.strip(), reqJsonStr)
        except Exception as err:
            Log.error('parseIncomeMsg(): The income message format is incorrect.')
            Log.exception(err)
            return('','',json.dumps({}))

    #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Function to handle the data-fetch/control request from the monitor-hub.
            Args:
                msg (str/bytes): _description_
            Returns:
                bytes: message bytes reply to the monitor hub side.
        """
        gv.gDebugPrint("Incomming message: %s" % str(msg), logType=gv.LOG_INFO)
        resp = b'REP;deny;{}'
        (reqKey, reqType, reqJsonStr) = self._parseIncomeMsg(msg)
        return resp

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function will be called by start(). """
        time.sleep(1)
        if self.udpServer:
            gv.gDebugPrint("Comm manager: udp server started.", logType=gv.LOG_INFO)
            self.udpServer.serverStart(handler=self.msgHandler)
        gv.gDebugPrint("Comm manager: udp server closed.", logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def fetchInfo(self, targetIP, msg):
        if self.udpClient:
            resp = self.udpClient.sendMsg(msg, resp=True,ipAddr=targetIP)
            if resp is None:
                gv.gDebugPrint('Target [%s] is not responsed.' %str(targetIP), logType=gv.LOG_WARN)
            else:
                return self._parseIncomeMsg(resp)
    
    #-----------------------------------------------------------------------------
    def disconnect(self):
        if self.udpServer: self.udpServer.serverStop()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class commManager(udpManager):

    def __init__(self) -> None:
        super().__init__()

    #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Function to handle the data-fetch/control request from the monitor-hub.
            Args:
                msg (str/bytes): _description_
            Returns:
                bytes: message bytes reply to the monitor hub side.
        """
        gv.gDebugPrint("Incomming message: %s" % str(msg), logType=gv.LOG_INFO)
        resp = b'REP;deny;{}'
        (reqKey, reqType, reqJsonStr) = self._parseIncomeMsg(msg)
        if reqKey=='GET':
            if reqType == 'data':
                rstStr = json.dumps(gv.iDataMgr.getResultDict())
                resp = ';'.join(('REP', 'data', rstStr))
        return resp
    
    #-----------------------------------------------------------------------------
    def postData(self, postUrl, jsonDict):
        try:
            res = requests.post(postUrl, json=jsonDict)
            if res.ok: gv.gDebugPrint("http server reply: %s" %str(res.json()), logType=gv.LOG_INFO)
        except Exception as err:
            gv.gDebugPrint("http server not reachable, error: %s" %str(err), logType=gv.LOG_ERR)

    #-----------------------------------------------------------------------------
    def reportTohub(self, jsonDict, udpMode=True):

        if udpMode and self.udpClient:
            ipaddress = (gv.gMonitorHubAddr['ipaddr'], gv.gMonitorHubAddr['udpPort'])
            reportStr = ';'.join(('POST', 'data', json.dumps(jsonDict)))
            self.udpClient.sendMsg(reportStr, resp=True, ipAddr=ipaddress)
        else:
            reportUrl = "http://%s:%s/dataPost/" % (gv.gMonitorHubAddr['ipaddr'], str(gv.gMonitorHubAddr['httpPort']))
            reportUrl += str(jsonDict['id'])
            jsonDict = {"rawData":json.dumps(jsonDict)}
            gv.gDebugPrint("Start to report monitorHub[%s]" %str(gv.gMonitorHubAddr['ipaddr']), logType=gv.LOG_INFO)
            self.postData(reportUrl, jsonDict)
