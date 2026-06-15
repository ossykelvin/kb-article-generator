from __future__ import annotations

import re


def _sentences(text: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip(' -•\n\t') for p in parts if p.strip()]


def offline_refine(article: str) -> str:
    cleaned = re.sub(r'\s+', ' ', article).strip()
    cleaned = cleaned.replace(' utilise ', ' use ')
    return cleaned


def offline_structure(user_prompt: str) -> dict:
    raw = user_prompt.split('REFINED ARTICLE:', 1)[-1].split('ARTICLE:', 1)[-1].strip()
    lines = [l.strip(' #*\t') for l in raw.splitlines() if l.strip()]
    title = lines[0][:90] if lines else 'Knowledge Base Article'
    body = ' '.join(lines[1:] if len(lines) > 1 else lines)
    sents = _sentences(body) or [body]
    overview = sents[0] if sents else 'This article explains the required process.'
    chunks = sents[1:] or sents
    steps = []
    for idx, sentence in enumerate(chunks[:8], 1):
        heading = sentence[:54].rstrip('.,:;') or f'Action {idx}'
        steps.append({'step_number': idx, 'heading': heading, 'details': [sentence]})
    if not steps:
        steps.append({'step_number': 1, 'heading': 'Review the request', 'details': [raw]})
    return {
        'title': title,
        'overview': overview,
        'steps': steps,
        'notes': ['Confirm any business-specific exceptions before sending the article to staff.'],
        'summary': 'Follow the steps above to complete the process consistently and support customers effectively.',
    }
