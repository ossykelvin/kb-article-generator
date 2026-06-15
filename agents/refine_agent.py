from __future__ import annotations

from agents.llm_client import LLMClient
from utils.config import Settings


def refine_article(raw_article: str, settings: Settings) -> str:
    client = LLMClient(settings)
    skill_prompt = client.prompt_from_skill(settings.skills_dir / 'refine_skill.md')
    user_prompt = f"Refine the following article according to the skill.\n\nARTICLE:\n{raw_article}"
    return client.generate_text(skill_prompt, user_prompt)
