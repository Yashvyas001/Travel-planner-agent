"""
Claude Service (stub)

This is a lightweight wrapper placeholder for Anthropic Claude integration.
It reads `CLAUDE_API_KEY` from config/environment and exposes `generate_text`.
For this educational project the implementation provides a safe fallback when
no key is configured.
"""
import os
import json
from typing import Dict, Any
from config import get_config
import requests


class ClaudeService:
    def __init__(self, config=None):
        self.config = config or get_config()
        self.api_key = os.getenv('CLAUDE_API_KEY', '') or getattr(self.config, 'CLAUDE_API_KEY', '')
        self.endpoint = os.getenv('CLAUDE_API_URL', '')

    def generate_text(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate text using Claude if API key is provided; otherwise return fallback."""
        if not self.api_key or not self.endpoint:
            # Fallback behaviour
            return f"[Claude fallback] {prompt[:300]}"

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'prompt': prompt,
                'max_tokens': max_tokens,
                'temperature': temperature
            }
            r = requests.post(self.endpoint, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
            # This will vary by Claude API shape; user must adapt with real API
            return data.get('text') or json.dumps(data)
        except Exception:
            return f"[Claude error fallback] {prompt[:300]}"


claude_service = ClaudeService()
