from __future__ import annotations

import json
import requests
from google import genai
from google.genai import types
from openai import OpenAI

from utils.config import Settings
from utils.helpers import extract_json_object, read_text_file


class AIClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.provider = settings.llm_provider

    def prompt_from_skill(self, skill_path):
        return read_text_file(skill_path)

    def _offline_response(self, system_prompt: str, user_prompt: str) -> str:
        article = user_prompt.split('ARTICLE:', 1)[-1].split('REFINED ARTICLE:', 1)[-1].strip()
        return article

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        merged_prompt = f"SYSTEM INSTRUCTION:\n{system_prompt}\n\nUSER REQUEST:\n{user_prompt}"
        if self.provider == 'offline':
            return self._offline_response(system_prompt, user_prompt)
        if self.provider == 'gemini':
            if not self.settings.gemini_api_key:
                raise ValueError('GEMINI_API_KEY is required when LLM_PROVIDER=gemini.')
            client = genai.Client(api_key=self.settings.gemini_api_key)
            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=merged_prompt,
                config=types.GenerateContentConfig(
                    temperature=self.settings.ai_temperature,
                    max_output_tokens=self.settings.ai_max_tokens,
                ),
            )
            return (response.text or '').strip()
        if self.provider == 'openai':
            if not self.settings.openai_api_key:
                raise ValueError('OPENAI_API_KEY is required when LLM_PROVIDER=openai.')
            client = OpenAI(api_key=self.settings.openai_api_key)
            response = client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}],
                temperature=self.settings.ai_temperature,
                max_tokens=self.settings.ai_max_tokens,
            )
            return (response.choices[0].message.content or '').strip()
        if self.provider == 'openrouter':
            if not self.settings.openrouter_api_key:
                raise ValueError('OPENROUTER_API_KEY is required when LLM_PROVIDER=openrouter.')
            headers = {
                'Authorization': f'Bearer {self.settings.openrouter_api_key}',
                'Content-Type': 'application/json',
                'X-Title': self.settings.openrouter_app_name,
            }
            if self.settings.openrouter_site_url:
                headers['HTTP-Referer'] = self.settings.openrouter_site_url
            payload = {
                'model': self.settings.openrouter_model,
                'messages': [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}],
                'temperature': self.settings.ai_temperature,
                'max_tokens': self.settings.ai_max_tokens,
            }
            r = requests.post(f"{self.settings.openrouter_base_url.rstrip('/')}/chat/completions", headers=headers, json=payload, timeout=90)
            r.raise_for_status()
            return (r.json()['choices'][0]['message']['content'] or '').strip()
        raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}. Use offline, gemini, openai, or openrouter.")

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        if self.provider == 'offline':
            from agents.offline_agent import offline_structure
            return offline_structure(user_prompt)
        json_instruction = user_prompt + "\n\nReturn ONLY a valid JSON object. Do not include markdown fences or extra text."
        text = self.generate_text(system_prompt, json_instruction)
        return extract_json_object(text)
