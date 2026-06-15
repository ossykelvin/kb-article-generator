from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from openai import OpenAI, AzureOpenAI

from utils.config import Settings
from utils.helpers import read_text_file


class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        provider = settings.llm_provider.lower().strip()
        if provider == 'azure_openai':
            if not settings.azure_openai_api_key or not settings.azure_openai_endpoint or not settings.azure_openai_deployment:
                raise ValueError('Azure OpenAI is selected but required Azure settings are missing.')
            self.client = AzureOpenAI(
                api_key=settings.azure_openai_api_key,
                azure_endpoint=settings.azure_openai_endpoint,
                api_version=settings.azure_openai_api_version,
            )
            self.model = settings.azure_openai_deployment
        else:
            if not settings.openai_api_key:
                raise ValueError('OPENAI_API_KEY is required when LLM_PROVIDER=openai.')
            kwargs = {'api_key': settings.openai_api_key}
            if settings.openai_base_url:
                kwargs['base_url'] = settings.openai_base_url
            self.client = OpenAI(**kwargs)
            self.model = settings.openai_model

    def prompt_from_skill(self, skill_path: Path) -> str:
        return read_text_file(skill_path)

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.settings.openai_temperature,
            max_tokens=self.settings.openai_max_tokens,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        )
        return (response.choices[0].message.content or '').strip()

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.settings.openai_temperature,
            max_tokens=self.settings.openai_max_tokens,
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
        )
        return json.loads((response.choices[0].message.content or '').strip())
