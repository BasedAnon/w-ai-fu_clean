import aiohttp
import os
from typing import Optional, Dict, Any
import base64
import json
import logging
import hashlib

class DirectAPI:
    """Direct implementation of NovelAI API without using the SDK"""
    
    def __init__(self):
        if "NAI_USERNAME" not in os.environ or "NAI_PASSWORD" not in os.environ:
            raise RuntimeError("Please ensure that NAI_USERNAME and NAI_PASSWORD are set in your environment")

        self.email = os.environ["NAI_USERNAME"]
        self.password = os.environ["NAI_PASSWORD"]
        
        self.logger = logging.getLogger("NovelAI")
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)
        
        self.api_token = None
        self.session = None
        
        # Base URLs
        self.base_url = "https://api.novelai.net"
        self.text_url = "https://api.novelai.net"  # Changed to match actual API
        self.image_url = "https://api.novelai.net/ai/generate-image"
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.login()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def login(self):
        """Login to NovelAI and get access token"""
        login_url = f"{self.base_url}/user/login"
        
        # Use email/password auth instead of key/secret
        login_data = {
            "email": self.email,
            "password": self.password
        }
        
        try:
            async with self.session.post(login_url, json=login_data) as response:
                if response.status != 201 and response.status != 200:
                    error_text = await response.text()
                    self.logger.error(f"Login failed with status {response.status}: {error_text}")
                    raise Exception("Authentication", 401, f"Login failed: {error_text}")
                
                data = await response.json()
                self.api_token = data.get("accessToken")
                
                if not self.api_token:
                    raise Exception("Authentication", 401, "No access token received")
                
                self.logger.info("Successfully authenticated with NovelAI")
        except aiohttp.ClientError as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise Exception("Connection", 502, str(e))
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication token for API requests"""
        if not self.api_token:
            raise ValueError("Not authenticated. Call login() first.")
        
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def generate_text(self, prompt: str, model: str = "kayra-v1", 
                           max_length: int = 80, temperature: float = 1.0,
                           repetition_penalty: float = 2.8,
                           repetition_penalty_range: int = 2048,
                           repetition_penalty_slope: float = 0.02,
                           length_penalty: float = 0.0,
                           stop_sequences: list = None) -> str:
        """Generate text from NovelAI's LLM models"""
        if not stop_sequences:
            stop_sequences = [[85], [198]]  # Default stop sequences
            
        url = f"{self.text_url}/ai/generate"
        
        # Updated payload to match NovelAI's expected format
        payload = {
            "input": prompt,
            "model": model,
            "parameters": {
                "use_string": True,
                "temperature": temperature,
                "max_length": max_length,
                "min_length": 1,
                "top_k": 12,
                "top_p": 0.95,
                "top_a": 0.75,
                "typical_p": 0.95,
                "tail_free_sampling": 0.975,
                "repetition_penalty": repetition_penalty,
                "repetition_penalty_range": repetition_penalty_range,
                "repetition_penalty_slope": repetition_penalty_slope,
                "repetition_penalty_frequency": 0.03,
                "repetition_penalty_presence": 0.0,
                "order": [
                    0, 1, 2, 3
                ]
            }
        }
        
        try:
            async with self.session.post(url, json=payload, headers=self.get_headers()) as response:
                if response.status != 200 and response.status != 201:
                    error_text = await response.text()
                    self.logger.error(f"Text generation failed with status {response.status}: {error_text}")
                    raise Exception("TextGeneration", response.status, error_text)
                
                data = await response.json()
                # Extract the generated text from the response
                output = data.get("output", "")
                return output
        except aiohttp.ClientError as e:
            self.logger.error(f"Connection error during text generation: {str(e)}")
            raise Exception("Connection", 502, str(e))
    
    async def generate_voice(self, text: str, voice: str, seed: int = -1, 
                            opus: bool = False, version: str = 'v2') -> bytes:
        """Generate voice using NovelAI's TTS service"""
        url = f"{self.base_url}/ai/generate-voice"
        
        payload = {
            "text": text,
            "voice": voice,
            "seed": seed,
            "opus": opus,
            "version": version
        }
        
        try:
            async with self.session.post(url, json=payload, headers=self.get_headers()) as response:
                if response.status != 200 and response.status != 201:
                    error_text = await response.text()
                    self.logger.error(f"Voice generation failed with status {response.status}: {error_text}")
                    raise Exception("VoiceGeneration", response.status, error_text)
                
                audio_data = await response.read()
                return audio_data
        except aiohttp.ClientError as e:
            self.logger.error(f"Connection error during voice generation: {str(e)}")
            raise Exception("Connection", 502, str(e))
