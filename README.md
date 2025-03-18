# W-AI-fu Clean

This is a modified version of [w-AI-fu](https://github.com/GXiaoyang/w-AI-fu_v2) that implements direct NovelAI API calls instead of using the NovelAI npm package.

## Important Requirements

- **Python 3.9** is required. This application will not work correctly with Python 3.10+ due to compatibility issues with some dependencies.
- NodeJS 16+ is recommended.

## Features

- Direct Python implementation of NovelAI API calls
- No dependency on NovelAI SDK
- Same functionality as the original w-AI-fu
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

## Troubleshooting

- If you encounter issues during installation, make sure Python 3.9 is installed and properly added to your PATH.
- If the installation script cannot find Python 3.9, you may need to modify the INSTALL.bat file to point to your specific Python 3.9 installation path.

## Credits

This project is a modification of [w-AI-fu by GXiaoyang](https://github.com/GXiaoyang/w-AI-fu_v2).
