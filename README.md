# AAS-VIDEO-STREAM
This repository is part of the Master's project conducted by Andreas Chanon Arnholm and Mathias Neslow Henriksen during the spring of 2021.

This code is related to the Asset Administration Shell (AAS) Video Stream hosting platform. The main aspect of this repository is a python script which contains an OPC UA Client which receives messages from an OPC UA Server located on the AAS. The messages are related to starting and stopping of robot video streams. The videos are streamed using WebGear API. The software has been tested with a Raspberry Pi 4 running Raspberry Pi OS 64bit. 

## Structure
Python scripts:
* [opcua_client.py](opcua_client.py): the script which contains the OPC UA client and its related functions.
* [streamer.py](streamer.py): the script which hosts each individual video streaming process.

## Setup
There are dependencies that need to be installed on the system before the AAS Video Streamer is fully functional.

Install the related python packages using pip:
    `$ pip3 install -r requirements.txt` 
