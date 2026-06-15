from __future__ import annotations

import re
from pathlib import Path

from utils.config import Settings
from utils.helpers import html_escape


def _extract_theme(template_html: str, settings: Settings) -> dict:
    gradient_match = re.search(r'linear-gradient\(135deg,\s*(#[0-9A-Fa-f]{3,6})\s*,\s*(#[0-9A-Fa-f]{3,6})\)', template_html)
    return {
        'outer_bg': settings.template_outer_bg,
        'width': settings.template_width,
        'header_gradient_start': gradient_match.group(1) if gradient_match else settings.template_header_gradient_start,
        'header_gradient_end': gradient_match.group(2) if gradient_match else settings.template_header_gradient_end,
        'body_bg': settings.template_body_bg,
        'card_bg': settings.template_card_bg,
        'text': settings.template_text_color,
        'muted': settings.template_muted_text_color,
        'border': settings.template_border_color,
        'accent': settings.template_accent_color,
    }


def _render_step_card(step: dict, theme: dict) -> str:
    detail_items = ''.join(f'<li>{html_escape(item)}</li>' for item in step.get('details', []))
    detail_block = f'<ul style="margin:0; padding-left:20px; font-size:14px; line-height:1.65; color:{theme["muted"]};">{detail_items}</ul>' if detail_items else ''
    image_block = ''
    image = step.get('image')
    if image:
        if image.get('is_placeholder'):
            image_block = (
                f'<div style="margin-top:14px; border:2px dashed {theme["accent"]}; border-radius:12px; padding:18px; text-align:center; color:{theme["muted"]}; background:#ffffff; font-size:13px;">{html_escape(image.get("caption", "Image placeholder"))}</div>'
            )
        else:
            image_block = (
                f'<div style="margin-top:14px;">'
                f'<img src="{image.get("data_uri", "")}" alt="{html_escape(image.get("alt_text", "Step image"))}" style="width:100%; max-width:100%; border-radius:12px; border:1px solid {theme["border"]}; display:block;" />'
                f'<div style="font-size:12px; color:{theme["muted"]}; margin-top:8px;">{html_escape(image.get("caption", ""))}</div>'
                f'</div>'
            )
    return (
        f'<div style="background:{theme["card_bg"]}; border-left:5px solid {theme["accent"]}; border-radius:10px; padding:16px 18px; margin:0 0 18px;">'
        f'<h3 style="margin:0 0 10px; font-size:16px; color:{theme["text"]};"><strong>Step {step.get("step_number")}: {html_escape(step.get("heading", ""))}</strong></h3>'
        f'{detail_block}{image_block}</div>'
    )


def render_html(article: dict, subtitle: str, intro_text: str, footer_text: str, settings: Settings) -> str:
    template_html = Path(settings.template_path).read_text(encoding='utf-8')
    theme = _extract_theme(template_html, settings)
    steps_html = ''.join(_render_step_card(step, theme) for step in article.get('steps', []))
    notes_html = ''.join(f'<li>{html_escape(note)}</li>' for note in article.get('notes', []))
    notes_block = ''
    if notes_html:
        notes_block = (
            f'<div style="background:{theme["card_bg"]}; border-left:5px solid {theme["accent"]}; border-radius:10px; padding:16px 18px; margin:0 0 18px;">'
            f'<h3 style="margin:0 0 10px; font-size:16px; color:{theme["text"]};"><strong>Notes</strong></h3>'
            f'<ul style="margin:0; padding-left:20px; font-size:14px; line-height:1.65; color:{theme["muted"]};">{notes_html}</ul>'
            f'</div>'
        )
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_escape(article.get('title', 'Knowledge Base Article'))}</title>
</head>
<body style="margin:0; padding:0; background:{theme['outer_bg']}; font-family:Arial, Helvetica, sans-serif; color:{theme['text']};">
<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background:{theme['outer_bg']}; padding:30px 15px;">
<tr><td align="center">
<table width="{theme['width']}" cellpadding="0" cellspacing="0" role="presentation" style="width:{theme['width']}px; max-width:100%; background:{theme['body_bg']}; border-radius:16px; overflow:hidden; box-shadow:0 8px 25px rgba(0,0,0,0.08);">
<tr><td style="background:linear-gradient(135deg,{theme['header_gradient_start']},{theme['header_gradient_end']}); padding:30px;">
<h1 style="margin:0; color:#ffffff; font-size:24px; line-height:1.3;">{html_escape(article.get('title', 'Knowledge Base Article'))}</h1>
<p style="margin:8px 0 0; color:#EAF1FF; font-size:14px;">{html_escape(subtitle)}</p>
</td></tr>
<tr><td style="padding:28px 30px 12px;">
<p style="margin:0 0 18px; font-size:15px; line-height:1.6;">Dear Team,</p>
<p style="margin:0 0 20px; font-size:15px; line-height:1.6;">{html_escape(intro_text)}</p>
<h2 style="margin:0 0 14px; font-size:20px; color:{theme['text']}; border-bottom:3px solid {theme['accent']}; padding-bottom:8px;">Overview</h2>
<p style="margin:0 0 18px; font-size:15px; line-height:1.6; color:{theme['muted']};">{html_escape(article.get('overview', ''))}</p>
<h2 style="margin:0 0 14px; font-size:20px; color:{theme['text']}; border-bottom:3px solid {theme['accent']}; padding-bottom:8px;">Procedural Steps</h2>
{steps_html}
{notes_block}
<h2 style="margin:0 0 14px; font-size:20px; color:{theme['text']}; border-bottom:3px solid {theme['accent']}; padding-bottom:8px;">Summary</h2>
<p style="margin:0 0 22px; font-size:15px; line-height:1.6; color:{theme['muted']};">{html_escape(article.get('summary', ''))}</p>
<p style="margin:0 0 6px; font-size:15px; line-height:1.6;">Regards,</p>
</td></tr>
<tr><td style="background:{theme['text']}; padding:18px 30px; color:#ffffff; font-size:12px; line-height:1.5;">{html_escape(footer_text)}</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


def render_text(article: dict, include_images: bool = False) -> str:
    lines = ['### **Overview**', article.get('overview', ''), '']
    for step in article.get('steps', []):
        lines.append(f"### **Step {step.get('step_number')}: {step.get('heading', '')}**")
        for detail in step.get('details', []):
            lines.append(f'- {detail}')
        if include_images and step.get('image'):
            image = step['image']
            if image.get('is_placeholder'):
                lines.append(f"[IMAGE PLACEHOLDER: {image.get('caption', '')}]")
            else:
                lines.append(f"[IMAGE: {image.get('name', '')}] - {image.get('caption', '')}")
        lines.append('')
    if article.get('notes'):
        lines.append('### **Notes**')
        for note in article.get('notes', []):
            lines.append(f'- {note}')
        lines.append('')
    lines.append('### **Summary**')
    lines.append(article.get('summary', ''))
    return '\n'.join(lines).strip()
