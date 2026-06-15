
# Skill: Image Placement

## Objective
Insert pictures at strategic locations in the knowledge base article based on the steps.

## Responsibilities
- Match available uploaded images to the most relevant steps.
- Use file names, captions, and article step descriptions to decide placement.
- If no suitable image is available for a step, create a helpful placeholder label.
- Keep image placement practical and minimal.

## Placement Rules
- Images should usually appear after the relevant step content.
- A step should not receive more than one image placement unless clearly required.
- Prioritize steps involving navigation, screens, menus, forms, confirmation messages, or outputs.

## JSON Output Schema
Return valid JSON only with this structure:
```json
{
  "placements": [
    {
      "step_number": 1,
      "image_name": "example.png",
      "alt_text": "Screenshot showing...",
      "caption": "Open the dashboard.",
      "placeholder_label": "Screenshot of dashboard page",
      "reason": "This image best supports the navigation step."
    }
  ]
}
```
