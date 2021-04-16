import sys
import os
import argparse
from time import sleep
from opcua import ua, Client
from threading import Thread


class CameraPubSub():
    def __init__(self, ua_obj):
        self.server_obj = ua_obj
        self.port = 9010
        self.i = 0
        self.sources = ["0", "theroom.mp4", "theroom.mp4"]

    def run_thread(self, source, port):
        os.system("python3 streamer.py --source " + source + " --port " + str(port))

    def event_notification(self, event):
        if event.Message.Text.lower() == "start":
            Thread(target=self.run_thread, args=(self.sources[self.i], str(self.port))).start()
            self.port += 1
            self.i += 1


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