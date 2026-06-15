# Skill: Image Placement

## Objective
Insert pictures at strategic locations in the knowledge base article based on the steps.

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
