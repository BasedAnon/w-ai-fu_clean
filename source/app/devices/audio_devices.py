import json
import sys
import os

def send_devices():
    # Return an empty device list since PyAudio is not required
    # for text-only input mode
    obj = {}
    print(json.dumps(obj), file=sys.stdout)

send_devices()
