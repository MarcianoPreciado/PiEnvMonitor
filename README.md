# PiEnvMonitor
Raspberry Pi based environmental monitor. Reports temperature and light level readings through TCP to a master Pi for logging and graphing.

# Usage
To run the logging server run
`python3 EnvMonitorMaster.py`
it will record the data recieved into a csv named after the label given to the remotes that connect and xfer.


To run the remote data collector with the label 'livingroom'
`python3 EnvMonitorRemote.py livingroom`
if a master is available to recieve, the data will be logged in livingroomm.csv
