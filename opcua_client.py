import sys
import os
import argparse
from time import sleep
from opcua import ua, Client
import subprocess

class CameraPubSub():
    def __init__(self, ua_obj):
        self.server_obj = ua_obj
        self.procs = {}

    def event_notification(self, event):
        action, rid, udp_url, stream_port = event.Message.Text.split(",")

        udp_url = "0"

        if action.lower() == "start" and rid not in self.procs:
            self.procs[rid] = subprocess.Popen(["python3", "streamer.py", "-s" + str(udp_url), "-p" + str(stream_port)])
        elif action.lower() == "stop" and rid in self.procs:
            self.procs[rid].terminate()
            self.procs.pop(rid, None)

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--domain')
    args = parser.parse_args(args=argv)

    """ 
        OPC UA CLIENT 
        For receiving commands from AAS
    """
    isConnected = False
    opcua_client = Client("opc.tcp://" + args.domain + ":4841/freeopcua/server/")

    while not isConnected:
        try:
            opcua_client.connect()
            isConnected = True
        except:
            print("Failed to connect on " + args.domain + " ... retrying")
            sleep(1)

    root = opcua_client.get_root_node()
    obj = root.get_child(["0:Objects", "2:MyObject"])

    camera_event = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:CameraEvent"])
    camera_publisher = CameraPubSub(obj)


    camera_sub = opcua_client.create_subscription(100, camera_publisher)
    camera_handle = camera_sub.subscribe_events(obj, camera_event)
    """ OPC UA CLIENT END """


if __name__ == '__main__':
    main()