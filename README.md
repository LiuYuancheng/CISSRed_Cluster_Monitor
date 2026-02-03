# **Building a Lightweight, Secure Cluster Monitor with InfluxDB and Grafana**

**Project Design Purpose** : This article walks through a lightweight, self-hosted server/VM cluster monitoring system built with Python, InfluxDB, and Grafana, designed specifically to handle the special or customized requirement for monitoring the  security labs, OT networks, or isolated clusters. Instead of relying on a black-box agent, you’ll build your own custom data collectors and monitor that fetch metrics from exactly the sources you need—whether that’s IPMI, network probes, or application-specific endpoints—and push them into a secure, local time-series database.

The practical example in this article is inspired by the CISS-Red_Cluster_Monitor project, which was developed to monitor a sandbox cluster (400+ VM) used for supporting a red team cybersecurity CTF competition. To make the design clear and reproducible, the article is structured around four main parts:

- **Core Idea** – The overall system architecture, including the agent/fetcher model and communication flow.
- **Security Design Choice: ** – How the system is designed to prevent participants from reverse-engineering agents or sending fake metrics.
- **Technology Stack** – The tools used (Python, InfluxDB, Grafana, etc.) and how to install and configure them.
- **Data and UI** – How data is stored, visualized in dashboards, and summarized or alerted (e.g., via Grafana and Telegram).

```python
# Author:      Yuancheng Liu
# Created:     2026/01/27
# Version:     v_0.2.1
# Copyright:   Copyright (c) 2025 Liu Yuancheng
# License:	   GNU General Public License
```

**Table of Contents**

[TOC]

------

### 1. Introduction

There are several tools in the market for supervising servers and VM clusters solutions like [PM2](https://pm2.keymetrics.io/) and similar platforms can monitor workload, network latency, and services running in Docker or virtual machines with very little setup. But some times we may have some special or customized requirement for monitoring the  security labs, OT networks, or isolated clusters, such as: 

- Can’t directly install agents on certain devices
- Need to collect power and hardware telemetry from sources like IPMI instead of OS-level agents
- The system must run in a fully local / air-gapped environment with no internet access
- Need to visualize the custom data collection and validation logic.

Based on these scenario and requirement, the monitoring system had to be: Simple and reliable under competition load, Secure against tampering or fake data injection, Deployable in a restricted network environment, and easy for administrators to visualize and audit in real time. 

#### 1.1 Usage Case Background And Objectives 

For example, the CISS-Red Stage One CTF event required continuous monitoring of multiple physical servers and virtual machines over a 48-hour period to ensure infrastructure stability and enable rapid incident response. The monitoring objective was to track key metrics in real time—including host servers CPU and memory usage, network latency, service availability of the CTF challenge VMs, and user SSH login activity—and to present all of this information through a centralized, intuitive dashboard. Whenever an abnormal condition was detected, the system would automatically send alert notifications to the support and administrator Telegram groups.



------

\2. System Architecture





We want to use the **Cluster Service Health Monitor** to create a simple dashboard to monitor the Computing cluster's resource usage (CPU%, RAM%) and network latency for the CISS-Red2023-CTF during the 48 event hours, so the NCL support and response the possible hardware problem in time during the event.

**LICENSE DECLARE**: 

```
This project is a test case of project [Cluster Service Health Monitor] with GNU General Public License. 

Cluster Service Health Monitor link:
https://github.com/LiuYuancheng/Cluster_Service_Health_Monitor
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

