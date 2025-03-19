import os
import base64
import json
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EnhancedDirectAPI")

class EnhancedDirectAPI:
    """
    Enhanced direct API client for NovelAI services.
    This class handles authentication and direct calls to the NovelAI API endpoints
    without relying on the NovelAI npm package.
    """
    
    # API Endpoints
    BASE_URL = "https://api.novelai.net"
    AUTH_ENDPOINT = "/user/login"
    TEXT_GENERATION_ENDPOINT = "/ai/generate"
    VOICE_GENERATION_ENDPOINT = "/ai/generate-voice"
    
    def __init__(self):
        """Initialize the API client."""
        self.access_token = None
        self.session = None
        self.use_api_key = os.environ.get("NAI_USE_API_KEY", "").lower() == "true"
        self.api_key = os.environ.get("NAI_API_KEY", "")
        self.username = os.environ.get("NAI_USERNAME", "")
        self.password = os.environ.get("NAI_PASSWORD", "")
        
        if self.use_api_key and not self.api_key:
            logger.error("API key mode is enabled but no API key is provided.")
        elif not self.use_api_key and (not self.username or not self.password):
            logger.error("Username/password mode is enabled but credentials are missing.")
    
    async def __aenter__(self):
        """Context manager entry point. Sets up session and authenticates."""
        self.session = aiohttp.ClientSession()
        if not self.access_token:  # Only authenticate if we don't have a token
            await self.authenticate()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point. Closes the session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def authenticate(self) -> bool:
        """
        Authenticate with NovelAI API using either API key or username/password.
        Returns True if authentication was successful, False otherwise.
        """
        if self.use_api_key:
            logger.info("Using API key authentication")
            self.access_token = self.api_key
            return True
        
        logger.info("Using username/password authentication")
        auth_data = {
            "key": self.username,
            "secret": self.password
        }
        
        try:
            async with self.session.post(
                f"{self.BASE_URL}{self.AUTH_ENDPOINT}",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status != 201:
                    error_text = await response.text()
                    logger.error(f"Authentication failed with status {response.status}: {error_text}")
                    raise Exception("Authentication", 401, f"Failed to authenticate: {error_text}")
                
                result = await response.json()
                self.access_token = result.get("accessToken")
                
                if not self.access_token:
                    logger.error("Authentication response did not contain an access token")
                    raise Exception("Authentication", 401, "No access token received")
                
                logger.info("Authentication successful")
                return True
        except aiohttp.ClientError as e:
            logger.error(f"Connection error during authentication: {str(e)}")
            raise Exception("Connection", 500, f"Connection error: {str(e)}")
    
    async def generate_text(self, prompt: str, model: str = "kayra-v1", **kwargs) -> Dict[str, Any]:
        """
        Generate text using NovelAI's text generation API.
        
        Args:
            prompt: The input text prompt
            model: The model to use (default: "kayra-v1")
            **kwargs: Additional generation parameters
            
        Returns:
            Dictionary containing the generated text and related information
        """
        if not self.access_token:
            await self.authenticate()
        
        # Default parameters
        params = {
            "input": prompt,
            "model": model,
            "parameters": {
                "use_string": True,
                "temperature": kwargs.get("temperature", 0.7),
                "max_length": kwargs.get("max_length", 100),
                "min_length": kwargs.get("min_length", 1),
                "top_k": kwargs.get("top_k", 0),
                "top_p": kwargs.get("top_p", 0.95),
                "tail_free_sampling": kwargs.get("tail_free_sampling", 0.975),
                "repetition_penalty": kwargs.get("repetition_penalty", 1.1),
                "repetition_penalty_range": kwargs.get("repetition_penalty_range", 1024),
                "repetition_penalty_slope": kwargs.get("repetition_penalty_slope", 0.18),
                "typical_p": kwargs.get("typical_p", 0.975),
                "length_penalty": kwargs.get("length_penalty", 1.0),
                "stop_sequences": kwargs.get("stop_sequences", []),
            }
        }
        
        headers = self._get_auth_headers()
        
        try:
            async with self.session.post(
                f"{self.BASE_URL}{self.TEXT_GENERATION_ENDPOINT}",
                json=params,
                headers=headers
            ) as response:
                if response.status != 201:
                    error_text = await response.text()
                    logger.error(f"Text generation failed with status {response.status}: {error_text}")
                    raise Exception("TextGeneration", response.status, f"Failed to generate text: {error_text}")
                
                result = await response.json()
                return {
                    "output": result.get("output", ""),
                    "error": None
                }
        except aiohttp.ClientError as e:
            logger.error(f"Connection error during text generation: {str(e)}")
            raise Exception("Connection", 502, f"Connection error: {str(e)}")
    
    async def generate_voice(
        self, text: str, voice: str, seed: int = -1, 
        opus: bool = False, version: str = "v2"
    ) -> bytes:
        """
        Generate voice audio using NovelAI's voice generation API.
        
        Args:
            text: The text to convert to speech
            voice: The voice seed to use
            seed: Random seed for generation
            opus: Whether to return opus format
            version: TTS version to use
            
        Returns:
            Binary audio data
        """
        if not self.access_token:
            await self.authenticate()
        
        params = {
            "text": text,
            "voice": voice,
            "seed": seed,
            "opus": opus,
            "version": version
        }
        
        headers = self._get_auth_headers()
        
        retry_count = 0
        max_retries = 3
        backoff_factor = 1.5
        
        while retry_count < max_retries:
            try:
                async with self.session.post(
                    f"{self.BASE_URL}{self.VOICE_GENERATION_ENDPOINT}",
                    json=params,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Voice generation failed with status {response.status}: {error_text}")
                        
                        # If rate limited, retry with exponential backoff
                        if response.status == 429 and retry_count < max_retries - 1:
                            retry_count += 1
                            wait_time = backoff_factor ** retry_count
                            logger.info(f"Rate limited, retrying in {wait_time} seconds...")
                            await asyncio.sleep(wait_time)
                            continue
                        
                        raise Exception("VoiceGeneration", response.status, f"Failed to generate voice: {error_text}")
                    
                    audio_data = await response.read()
                    return audio_data
            except aiohttp.ClientError as e:
                logger.error(f"Connection error during voice generation: {str(e)}")
                
                # Retry on connection errors
                if retry_count < max_retries - 1:
                    retry_count += 1
                    wait_time = backoff_factor ** retry_count
                    logger.info(f"Connection error, retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    continue
                
                raise Exception("Connection", 502, f"Connection error: {str(e)}")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get the authentication headers for API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "User-Agent": "w-AI-fu/2.0.0"
        }