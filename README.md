# CISS-Red2023-CTF_Cluster_Monitor

**Program Design Purpose** : We want to use the **Cluster Service Health Monitor** to create a simple dashboard to monitor the Computing cluster's resource usage (CPU%, RAM%) and network latency for the CISS-Red2023-CTF during the 48 event hours, so the NCL support and response the possible hardware problem in time during the event.

**LICENSE DECLARE**: 

```
This project is a test case of project [Cluster Service Health Monitor] with GNU General Public License. 

Cluster Service Health Monitor link:

```

[TOC]

------

### Introduction

This project is a test case of project [Cluster Service Health Monitor] to monitor the Computing cluster's resource usage (CPU%, RAM%) and network latency for the CISS-Red2023-CTF during the 48 event hours. 

##### System workflow diagram

The system workflow diagram is shown below. As the agent program are not compiled, to avoid the participant scan or send request to the monitor hub after checking the agent's code, we set the data committing mode to "Fetch mode", so the monitor will connect to the agent when it want to the data, the agent will only collected the data and save in their local storage. 

![](doc/img/workflow.png)

##### Dashboard UI

The main dashboard contents 22 small chart under 4 column, the column 1 and 2 will show the physical servers' CPU and Ram usage %, the column 3 and 4 will show the network latency.

![](doc/img/ui0.png)









config cmd:

```
mkdir monitorAgent
sudo timedatectl set-timezone Asia/Singapore
sudo vim /etc/resolv.conf
sudo apt install python3-pip
sudo pip3 install influxdb
sudo pip3 install pythonping
sudo pip3 install ntplib
sudo pip3 install psutil
git clone https://github.com/LiuYuancheng/CISSRed_Cluster_Monitor.git

sudo nohup python3 monitorAgent/CISSRed_Cluster_Monitor/src/client/AgentRun.py &

sudo nohup python3 AgentRun.py &

record the process:

sudo nohup python3 AgentRun.py &

ncl@cptest4:~$ sudo nohup python3 monitorAgent/CISSRed_Cluster_Monitor/src/client/AgentRun.py &
[1] 137511

163414

ps ax | grep AgetntRun.py

sudo systemctl start influxdb
```



```
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
> SHOW MEASUREMENTS ON monitorDB
> SHOW MEASUREMENTS ON gatewayDB
> USE monitorDB
Using database monitorDB
> SHOW MEASUREMENTS
> INSERT cpu,host=serverA value=10
> SHOW MEASUREMENTS
name: measurements
name
----
cpu
> exit
```

