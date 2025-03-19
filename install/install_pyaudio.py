import sys
import os
import urllib.request
import subprocess
from urllib.error import URLError

def main():
    # Detect Python version and architecture
    arch = "64" if sys.maxsize > 2**32 else "32"
    version = f"{sys.version_info.major}{sys.version_info.minor}"
    print(f"Detected Python {version}{arch}")

    # Only proceed if Python 3.9
    if version != "39":
        print("PyAudio auto-installation only supports Python 3.9")
        return False

    # Select the appropriate wheel URL
    wheel_url = ""
    wheel_filename = ""
    if arch == "64":
        wheel_url = "https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win_amd64.whl"
        wheel_filename = "PyAudio-0.2.11-cp39-cp39-win_amd64.whl"
    else:
        wheel_url = "https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.11-cp39-cp39-win32.whl"
        wheel_filename = "PyAudio-0.2.11-cp39-cp39-win32.whl"

    # Create temp directory if it doesn't exist
    os.makedirs(os.path.join("install", "temp"), exist_ok=True)
    wheel_path = os.path.join("install", "temp", wheel_filename)

    # Download the wheel
    print(f"Downloading PyAudio wheel from {wheel_url}...")
    try:
        urllib.request.urlretrieve(wheel_url, wheel_path)
    except URLError as e:
        print(f"Error downloading wheel: {e}")
        return False

    # Check if download was successful
    if not os.path.exists(wheel_path):
        print("Failed to download wheel file")
        return False

    filesize = os.path.getsize(wheel_path)
    if filesize < 1000:  # File too small, probably an error
        print(f"Downloaded file is too small ({filesize} bytes). Likely not a valid wheel.")
        return False

    # Install the wheel
    print(f"Installing PyAudio wheel ({filesize} bytes)...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", wheel_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Installation failed with code {result.returncode}")
        print(f"Error: {result.stderr}")
        return False
    else:
        print("PyAudio installed successfully.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
