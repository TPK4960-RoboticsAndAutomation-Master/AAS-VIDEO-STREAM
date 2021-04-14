import uvicorn
from vidgear.gears.asyncio import WebGear

class UDPStreamer:
    def __init__(self, input_stream, output_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream.split(":")[0]
        self.output_port = int(output_stream.split(":")[1])
        
        self.options = {
            "frame_size_reduction": 40,
            "frame_jpeg_quality": 80,
            "frame_jpeg_optimize": False,
            "frame_jpeg_progressive": False,
        }

    def run(self):
        web = WebGear(source=self.input_stream, logging=True, **self.options)
        uvicorn.run(web(), host=self.output_stream, port=self.output_port)
        web.shutdown()

udp_streamer = UDPStreamer("udp://10.22.23.227:5000","localhost:8080")
udp_streamer.run()