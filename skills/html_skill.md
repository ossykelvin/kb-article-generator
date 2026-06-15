# Skill: HTML Email Rendering

## Purpose
Render the structured knowledge base article into a professional, email-safe HTML layout using the supplied blue template.

## Design Requirements
- Use table-based outer layout for email compatibility.
- Use inline CSS because many email clients strip style blocks.
- Maintain the configured theme colours from `.env.local`.
- Use a 620px maximum content width unless changed in `.env.local`.
- Render major sections as Overview, Procedural Steps, Notes, and Summary.
- Render each step title as Header 3 Bold.
- Keep the design clean, staff-friendly, and suitable for Outlook-style email use.

## Content Requirements
- Include greeting, intro, article title, subtitle, body, notes, summary, and footer.
- Insert images or placeholders only where the image placement agent assigned them.
- Include image alt text.
- Escape unsafe HTML in article content.

## Controls
The app must support:
- Text output.
- Image placement output.
- HTML preview.
- HTML code view.
- Copy, download, and print actions where enabled.
