# Enhanced NovelAI API Implementation

This document describes the enhanced direct API implementation for NovelAI services in w-AI-fu.

## Overview

The enhanced implementation provides direct Python-based calls to the NovelAI API without relying on the NovelAI npm package. This implementation offers several advantages:

1. **Improved Error Handling**: Better detection and recovery from connection issues and API errors
2. **Detailed Logging**: More comprehensive logging for easier troubleshooting
3. **Connection Management**: Improved management of API connections to reduce timeouts and failures
4. **Configurable Options**: More granular control over API parameters

## How It Works

The enhanced implementation consists of the following components:

1. `enhanced_direct_api.py`: A core module that handles authentication, connection management, and direct calls to NovelAI services
2. `novel_tts_enhanced.py`: A module for text-to-speech services using the enhanced API
3. `novel_llm_enhanced.py`: A module for large language model services using the enhanced API
4. TypeScript interfaces to bridge these Python modules with the w-AI-fu application

## How to Enable the Enhanced API

You can enable the enhanced API implementation through the w-AI-fu user interface:

1. Go to the "Accounts" tab in the w-AI-fu settings
2. In the NovelAI section, check the "Use Enhanced API (improved reliability)" option
3. Save the settings

Note: This option is separate from the "Use API Key" option. You can use either email/password authentication or an API key with the enhanced API.

## Requirements

The enhanced API has the same requirements as the standard direct API:

- Python 3.7 or higher (Python 3.10 recommended)
- Required Python packages (automatically installed):
  - aiohttp
  - websockets

## Troubleshooting

The enhanced API implementation provides more detailed error messages for common issues:

- Authentication failures: Check your NovelAI credentials in the settings
- Connection timeouts: May indicate network issues or NovelAI service problems
- API rate limits: If you encounter rate limits, the enhanced API will retry with exponential backoff

## Technical Details

The enhanced API implementation makes direct HTTPS calls to the NovelAI API endpoints:

- `https://api.novelai.net/user/login` for authentication
- `https://api.novelai.net/ai/generate-voice` for TTS services
- `https://api.novelai.net/ai/generate` for LLM services

All communication is secured using standard HTTPS encryption.