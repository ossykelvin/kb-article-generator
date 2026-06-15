from __future__ import annotations

from agents.gemini_client import GeminiClient
from utils.config import Settings


def structure_article(refined_article: str, settings: Settings) -> dict:
    client = GeminiClient(settings)
    skill_prompt = client.prompt_from_skill(settings.skills_dir / 'structure_skill.md')
    user_prompt = f"Convert the following refined article into the required JSON schema.\n\nREFINED ARTICLE:\n{refined_article}"
    data = client.generate_json(skill_prompt, user_prompt)
    if 'steps' not in data or not isinstance(data['steps'], list):
        raise ValueError('Structured output is missing the steps array.')
    for index, step in enumerate(data['steps'], start=1):
        step.setdefault('step_number', index)
        step.setdefault('heading', f'Step {index}')
        step.setdefault('details', [])
    data.setdefault('notes', [])
    data.setdefault('overview', '')
    data.setdefault('summary', '')
    data.setdefault('title', 'Knowledge Base Article')
    return data
