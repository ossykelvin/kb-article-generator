# Knowledge Base Email Article Generator

This app converts a raw article into a staff-ready knowledge base article and renders it as an HTML email using the supplied blue template. It is designed for browser deployment, so you do not need to install software on your work device.

## Agent Flow

1. **Refinement Agent** - improves grammar, removes ambiguity, makes the tone suitable for customer service/support articles.
2. **Structure Agent** - converts the refined article into Overview, numbered steps, Notes, and Summary. Step headings are rendered as Header 3 Bold.
3. **Image Placement Agent** - places uploaded screenshots or placeholders at strategic points based on the article steps.
4. **HTML Email Agent** - applies the email template and blue theme, then produces previewable and downloadable HTML.

## Output Options

- **Text** - clean KB article text.
- **Image Plan** - article text with image markers and placement JSON.
- **HTML Preview** - rendered email preview.
- **HTML Code** - raw HTML for copying into an email tool.

Copy, download, and print controls can be enabled or disabled in `.env.local`.

## Recommended No-Installation Deployment

Use **Streamlit Community Cloud** or another hosted Python app platform.

### Streamlit Cloud Steps

1. Create a GitHub repository.
2. Upload all files from this folder to the repository.
3. In Streamlit Cloud, choose **New app** and select `app.py`.
4. Add your environment variables from `.env.example` into Streamlit **Secrets** or keep `.env.local` only for private local testing.
5. Deploy and open the generated browser URL.

## AI Provider Setup

Set `LLM_PROVIDER` to one of:

- `gemini`
- `openai`
- `openrouter`
- `offline`

`offline` works without API keys, but it uses simple rule-based formatting and is less intelligent.

## Important Environment Variables

Copy `.env.example` to `.env.local` for local/private use, then set:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

For OpenRouter:

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=openai/gpt-4.1-mini
```

For OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Local Run Command

Only use this if you are on a device where installs are allowed:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Template

The app uses `templates/email_template.html`, based on your uploaded blue email layout. Theme colours and content width are controlled from `.env.local`.

## Security Notes

- Do not commit real API keys to GitHub.
- Use Streamlit Secrets or platform environment variables for production.
- Uploaded images are embedded into the generated HTML as base64 data URIs. For very large emails, use smaller screenshots.
