# KB Article Generator (Gemini Edition, Deployment-Safe)

A browser-based multi-agent application that turns a raw article into a polished internal knowledge base article, places images strategically, and formats the result as an HTML email using the provided template.

## What this app does
1. Refines the source article for grammar, clarity, conciseness, and customer-service tone.
2. Converts the article into a structured KB format: Overview, steps, notes, and summary.
3. Maps uploaded images to the most relevant steps, or inserts placeholders when no images are supplied.
4. Renders a styled, email-safe HTML result using the template in `templates/email_template.html`.
5. Lets you switch between Text, Text + Images, HTML Preview, and HTML Code.
6. Supports Download, Copy, and Print.

## Deployment-safe fixes included
- `__init__.py` files already added in `agents`, `utils`, and `skills`
- `app.py` includes a `sys.path` root path fix for Streamlit Cloud / Replit imports
- Repo is structured so `app.py` sits at repository root

## Configure environment variables
Open `.env.local` and set:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=2400
```

## Deploy on Streamlit Community Cloud
1. Extract this ZIP.
2. Upload the **contents** of the project so `app.py` is at the repository root.
3. In Streamlit Community Cloud, select `app.py` as the entry point.
4. Add the environment values from `.env.local` to your Streamlit secrets or environment settings.
5. Deploy.

## Deploy on Replit
1. Extract this ZIP or import the repo from GitHub.
2. Add values from `.env.local` in Replit Secrets.
3. Use this run command:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
