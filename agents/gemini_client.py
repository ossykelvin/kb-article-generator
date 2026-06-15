from __future__ import annotations

from google import genai
from google.genai import types

from utils.config import Settings
from utils.helpers import extract_json_object, read_text_file


class GeminiClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        if settings.llm_provider.lower().strip() != "gemini":
            raise ValueError("This project is configured for Gemini only. Set LLM_PROVIDER=gemini.")
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required.")
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def prompt_from_skill(self, skill_path):
        return read_text_file(skill_path)

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        merged_prompt = f"SYSTEM INSTRUCTION:\n{system_prompt}\n\nUSER REQUEST:\n{user_prompt}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=merged_prompt,
            config=types.GenerateContentConfig(
                temperature=self.settings.gemini_temperature,
                max_output_tokens=self.settings.gemini_max_tokens,
            ),
        )
        return (response.text or "").strip()

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        merged_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_prompt}\n\n"
            f"USER REQUEST:\n{user_prompt}\n\n"
            "Return ONLY a valid JSON object. Do not include markdown fences or extra text."
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=merged_prompt,
            config=types.GenerateContentConfig(
                temperature=self.settings.gemini_temperature,
                max_output_tokens=self.settings.gemini_max_tokens,
                response_mime_type="application/json",
            ),
        )
        return extract_json_object(response.text or "")
