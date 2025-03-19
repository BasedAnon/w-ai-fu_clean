import os
import sys
import json
import asyncio
import threading
import uuid
import subprocess

# Try to import websockets, install it if not found
try:
    from websockets.sync.client import connect
except ImportError:
    print("Installing websockets package...", file=sys.stderr)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets==10.4"])
        from websockets.sync.client import connect
        print("Successfully installed websockets package.", file=sys.stderr)
    except Exception as e:
        print(f"Failed to install websockets package: {e}", file=sys.stderr)
        print("Please run: pip install websockets==10.4", file=sys.stderr)
        sys.exit(1)

try:
    import wave
    try:
        import pyaudio
        PYAUDIO_AVAILABLE = True
        audio = pyaudio.PyAudio()
    except ImportError:
        print("PyAudio not available. Audio output will be saved to files but not played.", file=sys.stderr)
        PYAUDIO_AVAILABLE = False
        audio = None
except ImportError:
    print("Wave module not available.", file=sys.stderr)
    sys.exit(1)

from boilerplate_direct import DirectAPI

os.system('title w-AI-fu NovelAI TTS Direct')

device_index = 0
interrupt_next = False

async def handle(message, websocket):
    split_message = message.split(' ');
    prefix = split_message[0]
    split_message.remove(prefix)
    payload = str.join(' ', split_message)
    match (prefix):
        case "GENERATE":
            await prepare_generate(payload, websocket)
        case "PLAY":
            await prepare_play(payload, websocket)
        case "INTERRUPT":
            interrupt()
    return

def interrupt():
    global interrupt_next
    interrupt_next = True

async def prepare_generate(payload, websocket):
    params = json.loads(payload)
    text = params["prompt"]
    options = params["options"]
    concurrent_id = params["concurrent_id"]
    response = ""
    try:
        response = await generate_tts(speak=text, voice_seed=options["voice_seed"])
    except Exception as e:
        if (len(e.args) < 2):
            print(e, file=sys.stderr)
            response = "ERROR UNDEFINED Could not get informations about this error. Sorry."
        else:
            match e.args[1]:
                case 401:
                    response = "ERROR WRONG_AUTH Missing or incorrect NovelAI mail and/or password."
                case 502:
                    response = "ERROR RESPONSE_FAILURE API Responded with 502. Service may be down or temporary inaccessible."
                case _:
                    print(e, file=sys.stderr)
                    response = "ERROR UNDEFINED " + str(e.args[2] if len(e.args) > 2 else e)
    websocket.send(str(concurrent_id) + " " + response)

async def prepare_play(payload, websocket):
    params = json.loads(payload)
    file_id = params["id"]
    options = params["options"]
    try:
        result = play_tts(file_id=file_id, device=options["device"], volume_modifier=options["volume_modifier"])
        if not result and not PYAUDIO_AVAILABLE:
            print(f"Audio file generated but not played (PyAudio not available): audio/{file_id}.wav", file=sys.stderr)
            print(f"To enable audio playback, install PyAudio manually.", file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
    websocket.send("PLAY DONE")

async def generate_tts(speak, voice_seed)-> str:
    async with DirectAPI() as api:
        text = speak
        voice = voice_seed # "Aini"
        seed = -1 #42
        opus = False
        version = 'v2'
        # Use our direct API instead of the SDK
        tts = await api.generate_voice(text, voice, seed, opus, version)
        new_id = str(uuid.uuid4())
        with open(f'audio/{new_id}.mp3', 'wb') as f:
            f.write(tts)
        return new_id

def play_tts(file_id, device = None, volume_modifier = 10):
    global audio, interrupt_next, device_index
    interrupt_next = False
    
    # Make sure the audio directory exists
    if not os.path.exists('audio'):
        os.makedirs('audio')
    
    # Convert .mp3 to .wav
    path = os.path.abspath(os.environ.get("CWD", ".") + '/bin/ffmpeg/ffmpeg.exe')

    if not os.path.isfile(path):
        print(f'Could not find ffmpeg at {path}. ffmpeg is not included in the w-AI-fu repository by default because of its size (> 100MB). If you cloned the repository, download the latest release instead: https://github.com/wAIfu-DEV/w-AI-fu/releases', file=sys.stderr)
        return False

    p = subprocess.run([path, '-loglevel', 'quiet', '-y', '-i', f'audio/{file_id}.mp3', '-filter:a', f'volume={str(volume_modifier)}dB', f'audio/{file_id}.wav'])
    
    if not PYAUDIO_AVAILABLE:
        # Just keep the .wav file when PyAudio is not available
        # but still return success - the TTS was successfully generated
        # We'll just keep the mp3 file for reference
        print(f"Generated audio file: audio/{file_id}.wav", file=sys.stderr)
        return True
    
    final_device = device_index
    if device != None:
        final_device = device

    # Open the wave file
    wave_file = wave.open(f'audio/{file_id}.wav', 'rb')
    # Open a stream for capturing audio from the virtual audio cable
    virtual_cable_stream = None
    try:
        virtual_cable_stream = audio.open(format=audio.get_format_from_width(wave_file.getsampwidth()),
                                        channels=wave_file.getnchannels(),
                                        rate=wave_file.getframerate(),
                                        output=True,
                                        output_device_index=final_device) # Set the input device index to the virtual audio cable
    except Exception as e:
        print('Cannot use selected audio device as output audio device.', file=sys.stderr)
        wave_file.close()
        return False
    # Read data from the wave file and capture it from the virtual audio cable
    data = wave_file.readframes(8192) #1024
    while data:
        if interrupt_next:
            interrupt_next = False
            break
        virtual_cable_stream.write(data)
        data = wave_file.readframes(8192)
    # Clean up resources
    virtual_cable_stream.stop_stream()
    virtual_cable_stream.close()
    wave_file.close()
    
    # Clean up files
    try:
        os.remove(f'audio/{file_id}.mp3')
        os.remove(f'audio/{file_id}.wav')
    except Exception as e:
        print(f"Error removing audio files: {e}", file=sys.stderr)
    
    return True

def prep_handle(message, websocket):
    asyncio.run(handle(message, websocket))

def clear_audio_files():
    if os.path.isdir('audio') == False:
        os.mkdir('audio')
        return
    dir_list = os.listdir('audio')
    for file in dir_list:
        try:
            os.remove('audio/' + file)
        except Exception as e:
            print(f"Error removing audio file {file}: {e}", file=sys.stderr)

async def main():
    clear_audio_files()
    with connect("ws://localhost:8766") as websocket:
        while True:
            message = websocket.recv()
            t = threading.Thread(target=prep_handle, args=[message, websocket])
            t.start()

if __name__ == '__main__':
    asyncio.run(main())
