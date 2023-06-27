#-----------------------------------------------------------------------------
# Name:        probGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2010/08/26
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os, sys

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('Prober', 'Agent')
TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir): sys.path.insert(0, gLibDir)
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

import ConfigLoader
CFG_FILE = 'agentConfig.txt'
gGonfigPath = os.path.join(dirpath, CFG_FILE)
print("Start to load config from config file: %s" %str(gGonfigPath))
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()

CONFIG_DICT = iConfigLoader.getJson()

#------<CONSTANTS>-------------------------------------------------------------
#UDP_PORT = int(CONFIG_DICT['HOST_PORT']) # host UDP port
#PROFILE_PATH = os.path.join(dirpath, CONFIG_DICT['PROFILE']+'.py')
#if not os.path.exists(PROFILE_PATH):
#    print("Error: The user proFile %s is not exist.Program exit!" %str(PROFILE_PATH))
#    exit()

DEBUG_FLG = False
LOG_INFO = 0
LOG_WARN = 1
LOG_ERR = 2
LOG_EXCEPT = 3

# the UDP ports
UDP_PORT = 3001

#-------<GLOBAL VARIABLES (start with "g")>-------------------------------------
def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

def gGetConfigVal(key, defaultVal=None):
    if key in CONFIG_DICT.keys(): 
        return CONFIG_DICT[key]
    return defaultVal

gOwnID = gGetConfigVal('OWN_ID', defaultVal='localhost')
gTestMode = gGetConfigVal('Test_Mode', defaultVal=False)

#-------<GLOBAL INSTANCES (start with "i")>-------------------------------------
iCommMgr = None
iDataMgr = None
iPortScanner = None
iNetProbeDriver = None
iLocalProbeDriver= None