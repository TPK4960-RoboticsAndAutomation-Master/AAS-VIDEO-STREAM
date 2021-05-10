import sys
import argparse
from time import sleep
from opcua import ua, Client
import subprocess
import os

def cl_green(msge): return '\033[32m' + msge + '\033[0m'

class CameraPubSub():
    def __init__(self, ua_obj):
        self.server_obj = ua_obj
        self.procs = {}

    def event_notification(self, event):
        action, rid, udp_url, stream_port = event.Message.Text.split(",")

        #udp_url = "0" #For testing with onboard laptop camera
        print(cl_green("INFO") + ":    ", "Incoming action:", action, "Robot:", rid)

        if action.lower() == "start" and rid not in self.procs:
            self.procs[rid] = subprocess.Popen(["python3", "streamer.py", "-s" + str(udp_url), "-p" + str(stream_port)])
        elif action.lower() == "stop" and rid in self.procs:
            print(cl_green("INFO") + ":    ", "Shutting down camera on", udp_url, "with PID:", self.procs[rid].pid)
            self.procs[rid].terminate()
            os.kill(self.procs[rid].pid, 9) #Hacky solution since webgear api will not shutdown if connenctions are open
            self.procs.pop(rid, None)
            print(cl_green("INFO") + ":    ", "Shutdown complete")

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--domain')
    args = parser.parse_args(args=argv)

    """ 
        OPC UA CLIENT 
        For receiving commands from AAS
    """
    isConnected = False
    opcua_client = Client("opc.tcp://" + args.domain + "/freeopcua/server/")

    while not isConnected:
        try:
            opcua_client.connect()
            isConnected = True
            print("Successfully connected with OPC UA server on: " + args.domain + ":4841")
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