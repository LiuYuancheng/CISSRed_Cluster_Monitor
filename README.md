# CISSRed_Cluster_Monitor

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

sudo nohup python monitorAgent/CISSRed_Cluster_Monitor/src/client/AgentRun.py &

record the process:
ncl@cptest4:~$ sudo nohup python3 monitorAgent/CISSRed_Cluster_Monitor/src/client/AgentRun.py &
[1] 137511

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

