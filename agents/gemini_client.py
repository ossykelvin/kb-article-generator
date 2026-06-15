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

    # ----------------------------------------
    # TEXT GENERATION
    # ----------------------------------------
def generate_text(self, system_prompt: str, user_prompt: str) -> str:
    try:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_prompt}\n\n{user_prompt}"}
                    ],
                }
            ],
            config=types.GenerateContentConfig(
                temperature=self.settings.gemini_temperature,
                max_output_tokens=self.settings.gemini_max_tokens,
            ),
        )
        return (response.text or "").strip()

    except Exception as e:
        print("\n🔥 GEMINI ERROR 🔥")
        print("Error:", str(e))

        # ✅ THIS LINE IS CRITICAL
        if hasattr(e, "response") and e.response is not None:
            try:
                print("Response JSON:", e.response.json())
            except Exception:
                pass

        if hasattr(e, "response_json"):
            print("Response JSON (alt):", e.response_json)

        raise

    # ----------------------------------------
    # JSON GENERATION
    # ----------------------------------------
