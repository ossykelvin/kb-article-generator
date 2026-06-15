from __future__ import annotations

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from agents.refine_agent import refine_article
from agents.structure_agent import structure_article
from agents.image_agent import plan_image_placements, attach_images_to_article
from agents.html_agent import render_html, render_text
from utils.config import load_settings
from utils.helpers import file_to_data_uri, normalize_newlines, to_json_string

settings = load_settings()
st.set_page_config(page_title=settings.app_title, page_icon=settings.page_icon, layout='wide')


def copy_button(content: str, key: str, label: str = 'Copy'):
    safe = json.dumps(content)
    components.html(
        f"<button onclick='navigator.clipboard.writeText({safe})' style=\"padding:8px 14px; border:none; border-radius:8px; background:#2563EB; color:#fff; cursor:pointer;\">{label}</button>",
        height=42,
        key=key,
    )


def print_button(html_content: str, key: str, label: str = 'Print'):
    safe = json.dumps(html_content)
    js = (
        f"<button onclick='(function(){{const html={safe}; const w=window.open(\"\", \"_blank\"); w.document.open(); w.document.write(html); w.document.close(); w.focus(); setTimeout(function(){{w.print();}}, 400);}})()' "
        f"style=\"padding:8px 14px; border:none; border-radius:8px; background:#111827; color:#fff; cursor:pointer;\">{label}</button>"
    )
    components.html(js, height=42, key=key)


def render_preview(html_content: str):
    components.html(html_content, height=900, scrolling=True)


st.title(settings.app_title)
st.caption('Gemini edition: paste an article, generate a polished KB article, place images strategically, and produce an HTML email using your template.')

with st.sidebar:
    st.subheader('Output & Email Options')
    st.caption(f"Model: {settings.gemini_model}")
    default_idx = settings.output_modes.index(settings.default_output_mode) if settings.default_output_mode in settings.output_modes else 0
    output_mode = st.selectbox('Output mode', settings.output_modes, index=default_idx)
    subtitle = st.text_input('Email subtitle', value=settings.default_subtitle)
    intro_text = st.text_area('Intro text', value=settings.default_intro_text, height=90)
    footer_text = st.text_area('Footer text', value=settings.default_footer_text, height=90)

with st.form('generator_form', clear_on_submit=False):
    article_title_override = st.text_input('Optional title override')
    source_article = st.text_area('Paste the source article', height=320, placeholder='Paste the raw article here...')
    uploaded_files = st.file_uploader('Upload step images (optional)', type=['png', 'jpg', 'jpeg', 'gif', 'webp'], accept_multiple_files=True)
    submit = st.form_submit_button('Generate KB Article')

if 'generated' not in st.session_state:
    st.session_state.generated = None

if submit:
    cleaned_article = normalize_newlines(source_article)
    if not cleaned_article:
        st.error('Please paste an article before generating output.')
    else:
        with st.spinner('Running the Gemini multi-agent flow...'):
            uploaded_images = []
            for file in uploaded_files or []:
                file_bytes = file.read()
                uploaded_images.append({
                    'name': file.name,
                    'mime_type': file.type,
                    'caption_hint': file.name.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' '),
                    'data_uri': file_to_data_uri(file_bytes, file.name, file.type),
                })
            refined = refine_article(cleaned_article, settings)
            structured = structure_article(refined, settings)
            if article_title_override.strip():
                structured['title'] = article_title_override.strip()
            placement_plan = plan_image_placements(structured, uploaded_images, settings)
            enriched_article = attach_images_to_article(structured, placement_plan, uploaded_images, settings)
            html_output = render_html(enriched_article, subtitle=subtitle, intro_text=intro_text, footer_text=footer_text, settings=settings)
            text_output = render_text(enriched_article, include_images=False)
            image_text_output = render_text(enriched_article, include_images=True)
            st.session_state.generated = {
                'timestamp': datetime.utcnow().isoformat(),
                'refined': refined,
                'structured': structured,
                'placement_plan': placement_plan,
                'enriched_article': enriched_article,
                'html_output': html_output,
                'text_output': text_output,
                'image_text_output': image_text_output,
            }

result = st.session_state.generated
if result:
    st.divider()
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.subheader('Selected Output')
    with col_b:
        st.caption(f"Generated UTC: {result['timestamp']}")

    if output_mode == 'Text':
        st.code(result['text_output'], language='markdown')
        if settings.enable_copy:
            copy_button(result['text_output'], key='copy_text', label='Copy text')
        if settings.enable_download:
            st.download_button('Download text', result['text_output'], file_name='kb_article.txt', mime='text/plain')
    elif output_mode == 'Text + Images':
        st.code(result['image_text_output'], language='markdown')
        if settings.enable_copy:
            copy_button(result['image_text_output'], key='copy_text_images', label='Copy text + image markers')
        if settings.enable_download:
            st.download_button('Download text + image markers', result['image_text_output'], file_name='kb_article_with_images.txt', mime='text/plain')
    elif output_mode == 'HTML Code':
        st.code(result['html_output'], language='html')
        if settings.enable_copy:
            copy_button(result['html_output'], key='copy_html', label='Copy HTML')
        if settings.enable_download:
            st.download_button('Download HTML', result['html_output'], file_name='kb_article.html', mime='text/html')
        if settings.enable_print:
            print_button(result['html_output'], key='print_html_code', label='Print HTML')
    elif output_mode == 'HTML Preview':
        render_preview(result['html_output'])
        action_cols = st.columns(3)
        with action_cols[0]:
            if settings.enable_download:
                st.download_button('Download HTML', result['html_output'], file_name='kb_article.html', mime='text/html')
        with action_cols[1]:
            if settings.enable_copy:
                copy_button(result['html_output'], key='copy_html_preview', label='Copy HTML')
        with action_cols[2]:
            if settings.enable_print:
                print_button(result['html_output'], key='print_html_preview', label='Print HTML')

    with st.expander('Show refined article'):
        st.write(result['refined'])
    with st.expander('Show structured JSON'):
        st.code(to_json_string(result['structured']), language='json')
    with st.expander('Show image placement plan'):
        st.code(to_json_string(result['placement_plan']), language='json')
else:
    st.info('Generate an article to preview text, image placement markers, or the HTML output.')
