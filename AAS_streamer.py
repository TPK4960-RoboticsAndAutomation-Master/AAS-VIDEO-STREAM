from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from vidgear.gears.asyncio import WebGear
import uvicorn
import asyncio


class AASStreamer:
    def __init__(self):
        self.app = Starlette(debug=True, routes=[Route('/', self.homepage)])
        
        self.options = {
            "frame_size_reduction": 40,
            "frame_jpeg_quality": 80,
            "frame_jpeg_optimize": False,
            "frame_jpeg_progressive": False,
        }

    async def homepage(self, request):
        return JSONResponse({'hello': 'world'})

    async def append_new_stream(self, input_stream, robot_id):
        web = WebGear(source=input_stream, logging=True, **self.options)
        self.app.mount("/robot/" + str(robot_id), web())

    def run(self):
        uvicorn.run(self.app, host="localhost", port=8080)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    
    aas_streamer = AASStreamer()
    loop.create_task(aas_streamer.run())
    

    while True:
        source = int(input("Source: "))
        robot_id = int(input("Robot ID: "))
        
        loop.create_task(aas_streamer.append_new_stream(source,robot_id))
        