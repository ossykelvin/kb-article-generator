# KB Article Generator (Gemini Edition)

A browser-based multi-agent application that turns a raw article into a polished internal knowledge base article, places images strategically, and formats the result as an HTML email using the provided template.

## What this app does
1. Refines the source article for grammar, clarity, conciseness, and customer-service tone.
2. Converts the article into a structured KB format: Overview, steps, notes, and summary.
3. Maps uploaded images to the most relevant steps, or inserts placeholders when no images are supplied.
4. Renders a styled, email-safe HTML result using the template in `templates/email_template.html`.
5. Lets you switch between Text, Text + Images, HTML Preview, and HTML Code.
6. Supports Download, Copy, and Print.

## Tech stack
- Python + Streamlit for the browser UI
- Google Gemini API via the `google-genai` SDK for agent tasks
- No local installation required on your device if you deploy to Streamlit Community Cloud or Replit

## Project structure
```text
kb-article-generator-gemini/
├── app.py
├── requirements.txt
├── .env.local
├── README.md
├── .streamlit/
│   └── config.toml
├── agents/
│   ├── gemini_client.py
│   ├── refine_agent.py
│   ├── structure_agent.py
│   ├── image_agent.py
│   └── html_agent.py
├── utils/
│   ├── config.py
│   └── helpers.py
├── skills/
│   ├── refine_skill.md
│   ├── structure_skill.md
│   ├── image_skill.md
│   └── html_skill.md
└── templates/
    └── email_template.html
```

## Configure environment variables
Open `.env.local` and set:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.5-pro
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=2400
```

> Get your Gemini API key from Google AI Studio.

## Run locally (optional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy without installing anything on your device
### Option 1: Streamlit Community Cloud (recommended)
1. Create a GitHub repository and upload this project.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Choose your repository, branch, and `app.py` as the entry point.
5. Add the values from `.env.local` into your Streamlit app secrets/settings.
6. Deploy the app.

### Option 2: Replit
1. Create a new Repl or import this project from GitHub.
2. Add the values from `.env.local` in Replit Secrets.
3. Set the run command to:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
4. Run and publish from the browser.

## Recommended Gemini models
- `gemini-2.5-flash` for fast draft generation
- `gemini-2.5-pro` for higher-quality final output

## Notes
- Keep real secrets out of GitHub if the repository is public.
- `.env.local` is included here as a ready configuration template; replace placeholder values before deployment.
- The app automatically reads the markdown skill files, so you can refine behavior without changing Python code.
- The HTML renderer uses the attached template in `templates/email_template.html` as its visual basis.
