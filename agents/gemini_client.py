from __future__ import annotations

from google import genai
from google.genai import types

from utils.config import Settings
from utils.helpers import extract_json_object, read_text_file


class GeminiClient:
    def __init__(self, settings: Settings):
        self.settings = settings

        if settings.llm_provider.lower().strip() != "gemini":
            raise ValueError(
                "This project is configured for Gemini only. Set LLM_PROVIDER=gemini."
            )

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required.")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def prompt_from_skill(self, skill_path: str) -> str:
        return read_text_file(skill_path)

    def _log_gemini_error(self, exc: Exception) -> None:
        print("\n=== GEMINI API ERROR ===")
        print(f"Type: {type(exc).__name__}")
        print(f"Message: {exc}")

        # Newer SDKs may expose one or more of these
        if hasattr(exc, "status_code"):
            try:
                print(f"Status code: {exc.status_code}")
            except Exception:
                pass

        if hasattr(exc, "response_json"):
            try:
                print("response_json:", exc.response_json)
            except Exception:
                pass

        if hasattr(exc, "response") and exc.response is not None:
            try:
                print("response.text:", exc.response.text)
            except Exception:
                pass
            try:
                print("response.json():", exc.response.json())
            except Exception:
                pass

        print("========================\n")

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=self.settings.gemini_temperature,
                    max_output_tokens=self.settings.gemini_max_tokens,
                ),
            )
            return (response.text or "").strip()

        except Exception as e:
            self._log_gemini_error(e)
            raise

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=(
                    user_prompt
                    + "\n\nReturn ONLY a valid JSON object. "
                      "Do not include markdown, explanations, or extra text."
                ),
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=self.settings.gemini_temperature,
                    max_output_tokens=self.settings.gemini_max_tokens,
                    response_mime_type="application/json",
                ),
            )
            return extract_json_object(response.text or "")

        except Exception as e:
            self._log_gemini_error(e)
            raise
``
