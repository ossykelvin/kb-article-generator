# Skill: Strategic Image Placement

## Purpose
Decide where uploaded screenshots, diagrams, or images should appear in the knowledge base article.

## Placement Principles
- Place images immediately after the step where they provide the most clarity.
- Prefer screenshots near navigation, form entry, approval, review, confirmation, or completion steps.
- Do not place an image in the Overview unless it is a broad process diagram or landing page screenshot.
- Do not overload the article with images. If multiple uploaded images are similar, use the clearest one only.
- If no images are uploaded and placeholders are enabled, insert useful screenshot placeholders for steps where staff would benefit from visual guidance.

## Caption Standards
Each image must have:
- A concise caption explaining what the staff member should notice.
- Alt text that describes the image for accessibility.
- A placement reason explaining why it belongs at that step.

## JSON Schema
Return exactly this JSON object shape:
{
  "placements": [
    {
      "step_number": 1,
      "image_name": "uploaded-file-name-or-placeholder",
      "caption": "string",
      "alt_text": "string",
      "reason": "string"
    }
  ]
}

## Constraints
- Do not generate new images.
- Do not invent uploaded file names.
- If placeholders are needed, use image_name as "placeholder".
- Return JSON only.
