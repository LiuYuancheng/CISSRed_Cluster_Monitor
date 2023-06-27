#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        BgCtrl.py
#
# Purpose:     This module is used to create a background program controller: 
#              When we want to run a program in back ground with a loop inside,
#              some time it is difficult for us to track whether the program is 
#              running or stopped if there are lots of other similar background 
#              programs are also running. This module is used to create a record 
#              file to record the current background program situation for the 
#              user to check and control.
#          
# Author:      Yuancheng Liu
#
# Created:     2020/08/31
# Copyright:   
# License:     
#-----------------------------------------------------------------------------
""" Program Design:
    The file "bgProgramRcd.txt" will be created in the same folder with this 
    module and used to record the program [ name, process ID, execution time].
    The 'bgProgramRcd.txt' is used as a flag to identify whether the program is 
    running: if the bgProgramRcd.txt exist and the process ID which saved in it 
    can also be found in the system, we think the program is running in the 
    back ground.

    When we want to check whether a program[A] uses this module is running in the 
    background, run the BgCtrl.py in the program[A]'s folder and input the control 
    cmd [Y/N]. If we want to stop the bgprogram, the bgProgramRcd.txt file will 
    be removed.

    For Windows system platform need to install lib: pip install psutil. Windows 
    platform can not use <os.kill(pid, 0)>

    For Linux system platform, when running the program need to conside the sudo 
    permission situion. Better to use sudo python BgCtrl.py: 
    - python3 bgProgram.py  + python 3 BgCtrl.py => work
    - python3 bgProgram.py  + sudo python 3 BgCtrl.py => work
    - sudo python3 bgProgram.py  + python 3 BgCtrl.py => not work
"""

import os
import datetime

BG_RCD = "bgProgramRcd.txt" # background program record

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class BgController(object):
    def __init__(self, progName):
        """ Init the controller.
        Args:
            progName ([str]): Name of the background execution program.
        """
        dirpath = os.path.dirname(__file__)
        self.progName = progName
        self.pId = os.getpid()
        self.rcdFile = os.path.join(dirpath, BG_RCD)
        try:
            with open(self.rcdFile, 'w') as fh:
                fh.write("Program Name\t: %s\n" % str(self.progName))
                fh.write("Process ID\t: %s\n" % str(self.pId))
                fh.write("Execute Time\t: %s\n" % str(datetime.datetime.now()))
            print("Created the background record file.")
        except Exception as e:
            print("Create the background record file failed: %s." % str(e))
            if os.path.exists(self.rcdFile):
                os.remove(self.rcdFile)

 #-----------------------------------------------------------------------------
    def bgRun(self):
        """ Check whether the program currently can be executed in the background. 
            return True/False.
        """
        return os.path.exists(self.rcdFile)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def processExist(pid):
    """""[Check whether a process is exist in the system.]""
    Args:
        pid ([int]): process 
    """
    if os.name == 'nt':
        from psutil import pid_exists  # >> pip install psutil
        return pid_exists(pid)
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True
    
#-----------------------------------------------------------------------------
def main(mode=0):
    print("Check the background program running situation:")
    processID = None
    dirpath = os.path.dirname(__file__)
    rcdFile = os.path.join(dirpath, BG_RCD)
    # Load the record file.
    if os.path.exists(rcdFile):
        with open(rcdFile, 'r') as fh:
            for line in fh.readlines():
                print(line)
                if "Process ID" in line:
                    processID = int(line.rstrip().split(':')[-1])
    else:
        print("No background record file, the program is not running.")
        exit()

    if processExist(processID):
        print("The program is running. Do you want end it [Y/N]:")
    else:
        print(
            "The program is NOT running. Do you want to remove the record [Y/N]:")
    uInput = str(input()).lower()
    if uInput == 'y':
        os.remove(rcdFile)
        print("-> removed the program background record at the same time.\n")
    print("Finished.")

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
