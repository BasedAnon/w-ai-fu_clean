# W-AI-fu Clean

This is a modified version of [w-AI-fu](https://github.com/GXiaoyang/w-AI-fu_v2) that implements direct NovelAI API calls instead of using the NovelAI npm package.

## Important Requirements

- **Python 3.9** is required. This application will not work correctly with Python 3.10+ due to compatibility issues with some dependencies.
- NodeJS 16+ is recommended.

## Features

- Direct Python implementation of NovelAI API calls
- No dependency on NovelAI SDK
- Same functionality as the original w-AI-fu
- Text-only input (voice input disabled to avoid PyAudio installation issues)
- Toggle between SDK and direct API implementation

## Installation

1. **Install Python 3.9** from [Python's official website](https://www.python.org/downloads/release/python-3913/).
   - During installation, ensure you check "Add Python to PATH".
   - You can verify the installation by opening Command Prompt and typing `python --version`.

2. **Install NodeJS** (if not already installed) from [NodeJS official website](https://nodejs.org/).

3. **Clone this repository**:
   ```
   git clone https://github.com/BasedAnon/w-ai-fu_clean.git
   cd w-ai-fu_clean
   ```

4. **Run the INSTALL.bat** file:
   - The script will automatically search for Python 3.9 installation.
   - It will install both NodeJS and Python dependencies.

## Usage

The application behaves the same as the original w-AI-fu but uses direct API calls to NovelAI instead of their SDK.

By default, the application uses the direct API implementation. If you want to switch back to the SDK implementation, you can modify the `use_direct_api` flag in the `source/app/state/state.ts` file.

### Audio Functionality

- **Text-to-Speech (Output)**: The application will still generate audio via NovelAI's TTS system and convert it to WAV files. However, if PyAudio is not installed, the audio will be generated but not played through your speakers. The files will be saved to the `audio` directory.

- **Voice Input (Input)**: Voice input has been disabled by default to avoid PyAudio installation issues. The application will only use text input.

### Optional PyAudio Installation

If you want full audio functionality (both input and output):

1. Download and install PyAudio manually from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   ```
   pip install path\to\downloaded\PyAudio-0.2.11-cp39-cp39-win_amd64.whl
   ```
2. To enable voice input, you'll need to modify the dependency_loader.ts file to use InputSystemVoice when voice_input is true

## Troubleshooting

- If you encounter issues during installation, make sure Python 3.9 is installed and properly added to your PATH.
- If the installation script cannot find Python 3.9, you may need to modify the INSTALL.bat file to point to your specific Python 3.9 installation path.
- Make sure ffmpeg is installed (included in the w-AI-fu release) for audio conversion.

## Credits

This project is a modification of [w-AI-fu by GXiaoyang](https://github.com/GXiaoyang/w-AI-fu_v2).
