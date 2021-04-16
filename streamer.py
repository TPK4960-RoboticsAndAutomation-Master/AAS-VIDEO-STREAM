from numpy import source
import uvicorn
from vidgear.gears.asyncio import WebGear
import argparse
import sys

# various performance tweaks
options = {
    "frame_size_reduction": 40,
    "frame_jpeg_quality": 80,
    "frame_jpeg_optimize": True,
    "frame_jpeg_progressive": False,
}

def start_stream(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--source')
    parser.add_argument('-p', '--port')
    args = parser.parse_args(args=argv)

    stream_source = args.source

    if len(stream_source) == 1:
        stream_source = int(stream_source)

    # initialize WebGear app
    web = WebGear(
        source=stream_source, logging=False, **options
    )
    
    uvicorn.run(web(), host="localhost", port=int(args.port))

if __name__ == '__main__':
    start_stream()