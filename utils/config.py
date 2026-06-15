from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('.env.local')


def getenv_bool(name: str, default: str = 'false') -> bool:
    return os.getenv(name, default).strip().lower() in {'1', 'true', 'yes', 'y', 'on'}


@dataclass
class Settings:
    llm_provider: str
    gemini_api_key: str
    gemini_model: str
    gemini_temperature: float
    gemini_max_tokens: int
    app_title: str
    page_icon: str
    default_output_mode: str
    output_modes: list[str]
    enable_download: bool
    enable_copy: bool
    enable_print: bool
    max_upload_size_mb: int
    skills_dir: Path
    template_path: Path
    use_placeholders_when_no_images: bool
    image_placeholder_text: str
    default_subtitle: str
    default_intro_text: str
    default_footer_text: str
    template_outer_bg: str
    template_header_gradient_start: str
    template_header_gradient_end: str
    template_body_bg: str
    template_card_bg: str
    template_text_color: str
    template_muted_text_color: str
    template_border_color: str
    template_accent_color: str
    template_width: int


def load_settings() -> Settings:
    return Settings(
        llm_provider=os.getenv('LLM_PROVIDER', 'gemini').strip(),
        gemini_api_key=(os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY') or '').strip(),
        gemini_model=os.getenv('GEMINI_MODEL', 'gemini-2.5-pro').strip(),
        gemini_temperature=float(os.getenv('GEMINI_TEMPERATURE', '0.2').strip()),
        gemini_max_tokens=int(os.getenv('GEMINI_MAX_TOKENS', '2400').strip()),
        app_title=os.getenv('APP_TITLE', 'Knowledge Base Article Generator').strip(),
        page_icon=os.getenv('PAGE_ICON', '📰').strip(),
        default_output_mode=os.getenv('DEFAULT_OUTPUT_MODE', 'HTML Preview').strip(),
        output_modes=[m.strip() for m in os.getenv('OUTPUT_MODES', 'Text,Text + Images,HTML Preview,HTML Code').split(',') if m.strip()],
        enable_download=getenv_bool('ENABLE_DOWNLOAD', 'true'),
        enable_copy=getenv_bool('ENABLE_COPY', 'true'),
        enable_print=getenv_bool('ENABLE_PRINT', 'true'),
        max_upload_size_mb=int(os.getenv('MAX_UPLOAD_SIZE_MB', '15').strip()),
        skills_dir=Path(os.getenv('SKILLS_DIR', 'skills').strip()),
        template_path=Path(os.getenv('TEMPLATE_PATH', 'templates/email_template.html').strip()),
        use_placeholders_when_no_images=getenv_bool('USE_PLACEHOLDERS_WHEN_NO_IMAGES', 'true'),
        image_placeholder_text=os.getenv('IMAGE_PLACEHOLDER_TEXT', 'Add screenshot here').strip(),
        default_subtitle=os.getenv('DEFAULT_SUBTITLE', 'Knowledge Base Article').strip(),
        default_intro_text=os.getenv('DEFAULT_INTRO_TEXT', 'Please review the knowledge base article below.').strip(),
        default_footer_text=os.getenv('DEFAULT_FOOTER_TEXT', 'This article is prepared for internal staff distribution and customer service support.').strip(),
        template_outer_bg=os.getenv('TEMPLATE_OUTER_BG', '#F2F4F7').strip(),
        template_header_gradient_start=os.getenv('TEMPLATE_HEADER_GRADIENT_START', '#0D1B3D').strip(),
        template_header_gradient_end=os.getenv('TEMPLATE_HEADER_GRADIENT_END', '#2563EB').strip(),
        template_body_bg=os.getenv('TEMPLATE_BODY_BG', '#FFFFFF').strip(),
        template_card_bg=os.getenv('TEMPLATE_CARD_BG', '#F2F4F7').strip(),
        template_text_color=os.getenv('TEMPLATE_TEXT_COLOR', '#0D1B3D').strip(),
        template_muted_text_color=os.getenv('TEMPLATE_MUTED_TEXT_COLOR', '#24324B').strip(),
        template_border_color=os.getenv('TEMPLATE_BORDER_COLOR', '#D9E2F3').strip(),
        template_accent_color=os.getenv('TEMPLATE_ACCENT_COLOR', '#2563EB').strip(),
        template_width=int(os.getenv('TEMPLATE_WIDTH', '620').strip()),
    )
