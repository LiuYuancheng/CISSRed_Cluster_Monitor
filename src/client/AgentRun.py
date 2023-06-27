#-----------------------------------------------------------------------------
# Name:        AgentRun.py
#
# Purpose:     The executable file.
#              
# Author:      Yuancheng Liu 
#
# Version:     v_0.2
# Created:     2023/01/11
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import probeGlobal as gv
import Log
import networkServiceProber
import localServiceProber

import commManager
import probeAgent
import BgCtrl as bg

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def initGlobalVal():
    if gv.gBgctrl: gv.iBgctrler = bg.BgController("ProgAgent")
    gv.iNetProbeDriver = networkServiceProber.networkServiceProber(debugLogger=Log)
    gv.iLocalProbeDriver = localServiceProber.localServiceProber(gv.gOwnID, debugLogger=Log)
    gv.iCommMgr = commManager.commManager()
    gv.iCommMgr.initUDPServer(gv.UDP_PORT)
    gv.iCommMgr.start()

#-----------------------------------------------------------------------------
def initProbers(agent):
    gv.gDebugPrint('Start to init the probers', logType=gv.LOG_INFO)
     # add a prober to check the Forni
    prober1 = probeAgent.Prober('Internet', target='8.8.8.8')
    prober1.addProbAction(gv.iNetProbeDriver.checkPing)
    agent.addProber(prober1)

    prober15 = probeAgent.Prober('local', target='Local')
    def porbAction_151(target):
        configDict =  {
                'cpu': {'interval': 0.5, 'percpu': True},
                'ram': 0,
            }
        if gv.iLocalProbeDriver: 
            gv.iLocalProbeDriver.updateResUsage(configDict=configDict)
            return gv.iLocalProbeDriver.getLastResult()
    prober15.addProbAction(porbAction_151)
    agent.addProber(prober15)

#-----------------------------------------------------------------------------
def main():
    initGlobalVal()
    agent = probeAgent.ProbeAgent(gv.gOwnID, timeInterval=gv.gTimeInterval)
    initProbers(agent)
    print("startRun")
    agent.startRun()
    print('Finish')
    gv.iCommMgr.disconnect()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
