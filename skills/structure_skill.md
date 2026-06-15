# Skill: Knowledge Base Article Structuring

## Purpose
Transform the refined article into a consistent knowledge base structure for staff email distribution.

## Required Structure
The article must be arranged as:
- Title
- Overview
- Step 1
- Step 2
- Additional numbered steps as required
- Notes
- Summary

## Formatting Rules
- Each procedural step must have a short, clear heading.
- Step headings will later be rendered as Header 3 Bold.
- Each step must contain concise action bullets or explanatory bullets.
- The Overview must explain the purpose, scope, and when the article applies.
- Notes must contain warnings, exceptions, dependencies, prerequisites, or reminders.
- Summary must close with the expected outcome.

## JSON Schema
Return exactly this JSON object shape:
{
  "title": "string",
  "overview": "string",
  "steps": [
    {
      "step_number": 1,
      "heading": "string",
      "details": ["string"]
    }
  ],
  "notes": ["string"],
  "summary": "string"
}

## Constraints
- Do not add images.
- Do not add HTML.
- Do not include markdown fences.
- Do not invent missing operational facts.
- Use as many steps as needed, but keep each step focused on one action or concept.
