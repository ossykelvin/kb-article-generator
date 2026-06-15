from __future__ import annotations

from agents.ai_client import AIClient
from agents.offline_agent import offline_refine
from utils.config import Settings


def refine_article(article: str, settings: Settings) -> str:
    if settings.llm_provider == 'offline':
        return offline_refine(article)
    client = AIClient(settings)
    skill_prompt = client.prompt_from_skill(settings.skills_dir / 'refine_skill.md')
    user_prompt = f"Refine this source article for customer service knowledge base use.\n\nARTICLE:\n{article}"
    return client.generate_text(skill_prompt, user_prompt)
