import sys
import os
import json
import asyncio

try:
    from websockets.sync.client import connect
except ImportError:
    print("Warning: websockets module not found. Installing...", file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
    from websockets.sync.client import connect

# This is a compatibility wrapper that redirects to novel_llm_direct.py
# We do this instead of modifying the TypeScript code to look for a different file

from novel_llm_direct import *

# The main logic is imported from novel_llm_direct.py

if __name__ == '__main__':
    asyncio.run(main())
