import base64
import sys
import os
import json
import asyncio
import time
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

from boilerplate_direct import DirectAPI

os.system('title w-AI-fu NovelAI LLM Direct')

# Default model settings
DEFAULT_MODEL = "kayra"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_LENGTH = 80 
DEFAULT_REP_PEN = 1.1
DEFAULT_LENGTH_PENALTY = 1.0

async def handle(message: str, websocket, api_handler):
    split_message = message.split(' ');
    prefix = split_message[0]
    split_message.remove(prefix)
    payload = str.join(' ', split_message)
    match (prefix):
        case "GENERATE":
            await prepare_generate(payload, websocket, api_handler)


async def prepare_generate(payload, websocket, api_handler):
    parsed = json.loads(payload)
    prompt = parsed["prompt"]
    llm_params = parsed["config"]
    response = ''
    try:
        response = "TEXT " + await generate(prompt, llm_params, api_handler)
    except Exception as e:
        if (len(e.args) < 2):
            print(e, file=sys.stderr)
            response = "ERROR UNDEFINED Could not get information about this error. Sorry."
        else:
            match e.args[1]:
                case 401:
                    response = "ERROR WRONG_AUTH Missing or incorrect NovelAI mail and/or password."
                case 502:
                    response = "ERROR RESPONSE_FAILURE API Responded with 502. Service may be down or temporary inaccessible."
                case _:
                    print(e, file=sys.stderr)
                    response = "ERROR UNDEFINED " + str(e.args[2] if len(e.args) > 2 else e)
    websocket.send(response)


async def generate(custom_prompt, parameters, api_handler) -> str:
    # Using direct API instead of NovelAI SDK
    model = parameters.get("model", DEFAULT_MODEL).lower()
    max_length = parameters.get("max_output_length", DEFAULT_MAX_OUTPUT_LENGTH)
    temperature = parameters.get("temperature", DEFAULT_TEMPERATURE)
    rep_pen = parameters.get("repetition_penalty", DEFAULT_REP_PEN)
    length_penalty = parameters.get("length_penalty", DEFAULT_LENGTH_PENALTY)
    
    # Use our direct API implementation
    async with DirectAPI() as api:
        # Generate text using the parameters 
        response = await api.generate_text(
            prompt=custom_prompt,
            model=model,
            max_length=max_length,
            temperature=temperature,
            repetition_penalty=rep_pen,
            length_penalty=length_penalty,
        )
        return response


async def main():
    with connect("ws://localhost:8765") as websocket:
        try:
            # Using DirectAPI for LLM
            api_handler = None
            while(True):
                await handle(websocket.recv(), websocket, api_handler)
        except Exception as e:
            if hasattr(e, 'args') and len(e.args) > 1 and e.args[1] == 401:
                while(True):
                    websocket.recv()
                    websocket.send("ERROR WRONG_AUTH Missing or incorrect NovelAI mail and/or password.")
            else:
                websocket.send(f"ERROR UNDEFINED {str(e)}")


if __name__ == '__main__':
    asyncio.run(main())
