#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        udpComTest.py
#
# Purpose:     This module will provide a multi-thread test case program to test
#              the UDP communication lib module <udpCom.py> by using port 5005.
#              If any change is added in the module <udpCom.py>, please run this
#              test case to make sure the udpCom lib is still working.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/15
# Version:     v_0.2.0
# Copyright:   Copyright (c) 2019 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import time
import random
import string
import threading    # create multi-thread test case.
import udpCom

UDP_PORT = 5005
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class testServerThread(threading.Thread):
    """ Thread to test the UDP server/insert the tcp server in other program.""" 
    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        self.threadName = name
        self.server = udpCom.udpServer(None, UDP_PORT)

    def msgHandler(self, msg):
        """ The test handler method passed into the UDP server to handle the 
            incoming messages.
        """
        print("Incoming client message: %s" %str(msg))
        return msg

    def run(self):
        """ Start the udp server's main message handling loop."""
        print("Server thread run() start.")
        self.server.serverStart(handler=self.msgHandler)
        print("Server thread run() end.")
        self.threadName = None # set the thread name to None when finished.

    def setBufferSize(self, bufferSize):
        return self.server.setBufferSize(bufferSize)

    def stop(self):
        """ Stop the udp server. Create a end client to bypass the revFrom() block."""
        self.server.serverStop()
        endClient = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        endClient.disconnect()
        endClient = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def showTestResult(expectVal, val, message):
    rst = "[o] %s pass." %message if val == expectVal else "[x] %s error, expect:%s, get: %s." %(message, str(expectVal), str(val))
    print(rst)
    return val == expectVal

def getRandomStr(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def msgHandler(msg):
    """ The test handler method passed into the UDP server to handle the 
        incoming messages.
    """
    print("Incoming client message: %s" % str(msg))
    return msg

#-----------------------------------------------------------------------------
def testCase(mode):
    print("Start UDP client-server test. test mode: %s \n" % str(mode))
    testResultList = [] # test fail count and test pass flag.
    if mode == '0':
        print("Start the UDP Server.")
        serverThread = testServerThread(None, 0, "server thread")
        serverThread.start()
        time.sleep(1)
        print("Start the UDP Client.")
        client = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        # test case 0
        print("[0] client heart beat message test:")
        tPass = True
        for i in range(3):
            msg = "- Client test data %s" % str(i)
            resp = client.sendMsg(msg, resp=True).decode('UTF-8')
            tPass &= showTestResult(msg, resp, 'heart beat test %s' %str(i))
        testResultList.append(tPass)
        # test case 1
        print("[1] Client disconnect test:")
        client.disconnect()
        rst = client.sendMsg('Testdata', resp=True)
        tPass = showTestResult(None, rst, 'A closed client send message again.')
        testResultList.append(tPass)
        # test case 2
        print("[2] Server stop test:")
        serverThread.stop()
        time.sleep(1)  # wait 1 second for all the UDP socket close.
        client = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        rst = client.sendMsg('Testdata', resp=True)
        tPass = showTestResult(None, rst, 'A closed server not accept message again.')
        testResultList.append(tPass)
    
        client = serverThread = None
        print(" => All test finished: %s/%s" % (str(testResultList.count(True)), str(len(testResultList))))
    elif mode == '1':
        print(" - Please input the UDP port: ")
        udpPort = int(str(input()))
        server = udpCom.udpServer(None, udpPort)
        server.serverStart(handler=msgHandler)
        print("Start the UDP echo server listening port [%s]" % udpPort)
    elif mode == '2':
        print(" - Please input the IP address: ")
        ipAddr = str(input())
        print(" - Please input the UDP port: ")
        udpPort = int(str(input()))
        client = udpCom.udpClient((ipAddr, udpPort))
        while True:
            print(" - Please input the message: ")
            msg = str(input())
            resp = client.sendMsg(msg, resp=True)
            print(" - Server resp: %s" % str(resp))
    elif mode == '3':
        print("Start message bigger than buffer size test. test mode: %s \n" % str(mode))
        testBFSize = 100
        wrongBFSize = 100000000
        serverThread = testServerThread(None, 0, "server thread")
        rst = serverThread.setBufferSize(wrongBFSize)
        print(" - Set wrong bufferSize test [server] passed: %s" %str(not rst) )
        client = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        rst = client.setBufferSize(wrongBFSize)
        print(" - Set wrong bufferSize test [client] passed: %s" %str(not rst) )
        serverThread.setBufferSize(testBFSize)
        client.setBufferSize(testBFSize)
        serverThread.start()
        print("Start the UDP Client.")

        msg = getRandomStr(400)

        rpl = client.sendChunk(msg, resp=True).decode('utf-8')
        print("Original message:")
        print(msg)
        print("Reply message:")
        print(rpl)
        showTestResult(msg, rpl, 'send big message bigger than buffer')
        serverThread.stop()
    else:
        print("Input %s is not valid, program terminate." % str(uInput))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    print("Run the testCase as a UDP\n\
        \t (0) Auto test,\n\
        \t (1) Start a UDP echo server,\n\
        \t (2) Start a UDP client\n\
        \t (3) Test send big message bigger than buffer")
    uInput = str(input('Input your choice:'))
    testCase(uInput)
