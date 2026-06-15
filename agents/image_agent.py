from __future__ import annotations

from typing import List, Dict, Any

from agents.llm_client import LLMClient
from utils.config import Settings


def plan_image_placements(article: dict, uploaded_images: List[Dict[str, Any]], settings: Settings) -> dict:
    client = LLMClient(settings)
    skill_prompt = client.prompt_from_skill(settings.skills_dir / 'image_skill.md')
    image_catalog = [
        {'name': item['name'], 'caption_hint': item.get('caption_hint', ''), 'mime_type': item.get('mime_type', '')}
        for item in uploaded_images
    ]
    user_prompt = (
        'Use the image placement skill to map images to steps.\n\n'
        f'ARTICLE JSON:\n{article}\n\n'
        f'UPLOADED IMAGES:\n{image_catalog}\n\n'
        f'PLACEHOLDERS ENABLED:\n{settings.use_placeholders_when_no_images}'
    )
    try:
        result = client.generate_json(skill_prompt, user_prompt)
    except Exception:
        result = {'placements': []}

    placements = result.get('placements', []) if isinstance(result, dict) else []
    valid_names = {img['name'] for img in uploaded_images}
    cleaned = []
    for placement in placements:
        step_number = int(placement.get('step_number', 0) or 0)
        if step_number <= 0:
            continue
        image_name = (placement.get('image_name') or '').strip()
        if image_name and image_name not in valid_names:
            image_name = ''
        cleaned.append({
            'step_number': step_number,
            'image_name': image_name,
            'alt_text': (placement.get('alt_text') or '').strip(),
            'caption': (placement.get('caption') or '').strip(),
            'placeholder_label': (placement.get('placeholder_label') or '').strip(),
            'reason': (placement.get('reason') or '').strip(),
        })

    if not cleaned:
        for step in article.get('steps', []):
            chosen = uploaded_images[step['step_number'] - 1]['name'] if len(uploaded_images) >= step['step_number'] else ''
            cleaned.append({
                'step_number': step['step_number'],
                'image_name': chosen,
                'alt_text': f"Illustration for {step.get('heading', '')}".strip(),
                'caption': step.get('heading', ''),
                'placeholder_label': f"{settings.image_placeholder_text}: {step.get('heading', '')}".strip(' :'),
                'reason': 'Fallback placement',
            })
    return {'placements': cleaned}


def attach_images_to_article(article: dict, placement_plan: dict, uploaded_images: List[Dict[str, Any]], settings: Settings) -> dict:
    image_lookup = {img['name']: img for img in uploaded_images}
    placements_by_step = {item['step_number']: item for item in placement_plan.get('placements', [])}
    enriched_steps = []
    for step in article.get('steps', []):
        placement = placements_by_step.get(step['step_number'], {})
        image_name = placement.get('image_name', '')
        image = image_lookup.get(image_name)
        step_copy = dict(step)
        if image:
            step_copy['image'] = {
                'name': image['name'],
                'data_uri': image['data_uri'],
                'alt_text': placement.get('alt_text') or image.get('caption_hint') or image['name'],
                'caption': placement.get('caption') or image.get('caption_hint') or image['name'],
                'is_placeholder': False,
            }
        elif settings.use_placeholders_when_no_images:
            step_copy['image'] = {
                'name': '',
                'data_uri': '',
                'alt_text': placement.get('placeholder_label') or settings.image_placeholder_text,
                'caption': placement.get('placeholder_label') or settings.image_placeholder_text,
                'is_placeholder': True,
            }
        else:
            step_copy['image'] = None
        enriched_steps.append(step_copy)
    enriched = dict(article)
    enriched['steps'] = enriched_steps
    return enriched
