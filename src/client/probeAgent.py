#-----------------------------------------------------------------------------
# Name:        probeAgent.py
#
# Purpose:     An agent program collects and schedules several different kinds 
#              of probers based on the customized config profile to check the 
#              entire service availably of a small cluster.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2023/03/09
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import json
from collections import OrderedDict

import probeGlobal as gv
# import own lib
import Log

import dataManager

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class Prober(object):
    """ The prober is a package object contents a list of probe action (with target 
        config) and provide the api to run them under their add in sequence.
    """
    def __init__(self, id, target='localHost', timeInterval=0.5) -> None:
        """ Init the prober, each prober can only aim to one target (ip/doman/local).
        Args:
            id (_type_): prober's ID
            target (str, optional): ip/doman/or Local. Defaults to 'localHost'.
            timeInterval (int, optional): probe function execute interval. Defaults to 0.5 sec.
        """
        self.probId = id
        self.target = target
        self.functionCount = 0
        self.probActionDict = OrderedDict()
        self.crtResultDict = {'target': self.target}
        self.timeInterval = timeInterval
        self.terminate = False

#-----------------------------------------------------------------------------
    def addProbAction(self, probActionRef):
        """ Add a probAction functino in the prober.    
            Args:
                probActionRef (_type_): function reference.
        """
        self.functionCount += 1
        actId = '-'.join((str(self.probId), str(self.functionCount)))
        self.probActionDict[actId] = probActionRef
        self.crtResultDict[actId] = {
            'time': time.time(),
            'result': {} }

#-----------------------------------------------------------------------------
    def executeProbeAction(self):
        if self.terminate: return 
        for probSet in self.probActionDict.items():
            actId, probAct = probSet
            gv.gDebugPrint('Execute probe action: %s' %str(actId), logType=gv.LOG_INFO)
            self.crtResultDict[actId]['time'] = time.time()
            try:
                rst = probAct(self.target)
                if isinstance(rst, dict): self.crtResultDict[actId]['result'].update(rst)
            except Exception as err:
                Log.exception(err)
                self.crtResultDict[actId]['result'] = None
            if self.timeInterval > 0: time.sleep(self.timeInterval)

#-----------------------------------------------------------------------------
    def getResult(self):
        """ Return all the probeAction executed result. Example of result dict:
             { "target": <ip>,
                "<id>-1": {
                    "time": <time>,
                    "result": {
                        "target": <ip/doman>,
                        "<functionName>": [<result>, ]
                    }
                 }, ...}
        """
        return self.crtResultDict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class ProbeAgent(object):
    """ Agent collects and schedules several different kinds of probers """

    def __init__(self, id, fetchMode=False, timeInterval=5) -> None:
        self.id = id
        self.fetchMode = fetchMode
        self.timeInterval = timeInterval
        gv.iDataMgr = dataManager.DataManager(self, fetchMode=False)
        self.proberDict = OrderedDict()
        self.crtResultDict = {'id': self.id}
        self.terminate = False

#-----------------------------------------------------------------------------
    def addProber(self, prober):
        if str(prober.probId) in self.proberDict.keys():
            gv.gDebugPrint("Prober %s was exist, can not add" %str(prober.probId), logType=gv.LOG_WARN)
        else:
            proberID = str(prober.probId)
            self.proberDict[proberID] = prober
            self.crtResultDict[proberID] = prober.getResult()

#-----------------------------------------------------------------------------
    def executeProbers(self):
        if self.terminate: return 
        for proberSet in self.proberDict.items():
            pId, prober = proberSet
            prober.executeProbeAction()
            self.crtResultDict[pId] = prober.getResult()
        gv.iDataMgr.archiveResult(self.crtResultDict)

#-----------------------------------------------------------------------------     
    def startRun(self):
        while not self.terminate:
            if not gv.gTestMode:
                self.executeProbers()
            time.sleep(1)
            if gv.iDataMgr:
                if gv.gTestMode:
                    print('load simulation data')
                    testFile = os.path.join(gv.DIR_PATH, 'test.json')
                    with open(testFile, 'r') as f:
                        data = json.load(f)
                        gv.iDataMgr.archiveResult(data)
                else:
                    gv.iDataMgr.archiveResult(self.crtResultDict)
                #gv.iCommMgr.reportTohub(gv.iDataMgr.getResultDict(), udpMode=False)
            time.sleep(self.timeInterval)
