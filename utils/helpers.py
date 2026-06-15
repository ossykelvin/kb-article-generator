from __future__ import annotations

import base64
import html
import json
import mimetypes
from pathlib import Path
from typing import Any


def read_text_file(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def to_json_string(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def file_to_data_uri(file_bytes: bytes, file_name: str, mime_type: str | None = None) -> str:
    guessed = mime_type or mimetypes.guess_type(file_name)[0] or 'application/octet-stream'
    encoded = base64.b64encode(file_bytes).decode('utf-8')
    return f'data:{guessed};base64,{encoded}'


def html_escape(text: str) -> str:
    return html.escape(text or '')


def normalize_newlines(text: str) -> str:
    return (text or '').replace('\r\n', '\n').replace('\r', '\n').strip()
