# NovelAI API Key Authentication Guide

This guide explains how to use the new NovelAI API key authentication feature in w-AI-fu.

## Why Use API Key Authentication?

The API key authentication method is more reliable than email/password authentication for several reasons:

1. API keys are specifically designed for programmatic access
2. API keys don't expire as quickly as login sessions
3. API keys avoid the various authentication errors that can occur with email/password login
4. The API key method is less susceptible to changes in NovelAI's authentication methods

## How to Get Your NovelAI API Key

1. Log in to your NovelAI account at [https://novelai.net/](https://novelai.net/)
2. Click on your account name in the top-right corner
3. Select "Account" from the dropdown menu
4. Scroll down to the "API Key" section
5. Click on "Generate" if you don't already have an API key
6. Copy the generated API key (it should be a long string of characters)

## Setting Up API Key Authentication in w-AI-fu

1. Open w-AI-fu
2. Go to the "Accounts" tab in Settings
3. In the NovelAI section, locate the "API Key" field
4. Paste your NovelAI API key into this field
5. Check the "Use API Key" checkbox to enable API key authentication
6. Click "Save" to apply your changes

![Settings UI showing API Key field](../docs/img/novelai_api_key_settings.png)

## Troubleshooting

If you're still experiencing authentication issues after setting up API key authentication:

1. Make sure your API key is correctly copied from NovelAI without any extra spaces
2. Check that the "Use API Key" checkbox is enabled
3. Verify that your NovelAI subscription is active
4. Try generating a new API key from your NovelAI account if the current one doesn't work

## Security Note

Your API key provides access to your NovelAI account, so keep it secure:

- Don't share your API key with others
- Don't post it online or in public repositories
- w-AI-fu stores your API key locally in an encrypted format

If you believe your API key has been compromised, generate a new one immediately from your NovelAI account settings.
