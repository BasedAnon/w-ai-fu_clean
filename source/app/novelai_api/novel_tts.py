#!/usr/bin/env python

import os
import sys
import json
import time

# Don't attempt to import any non-standard libraries
# Just act as a dummy service that returns empty responses

os.system('title w-AI-fu NovelAI TTS (Mock)')

print("WARNING: This is a mock TTS service. Audio generation is disabled.", file=sys.stderr)
print("To enable audio generation, install websockets and required dependencies:", file=sys.stderr) 
print("  pip install websockets==10.4", file=sys.stderr)

# Mock functions and main loop
def main():
    try:
        # Wait for a while to let the app initialize
        time.sleep(2)
        
        # Just print empty responses when expected
        while True:
            # Wait for input from the app (which we can't actually receive)
            # Just sleep to prevent this script from consuming CPU
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("TTS Mock service shutting down", file=sys.stderr)
    except Exception as e:
        print(f"Error in TTS Mock service: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
