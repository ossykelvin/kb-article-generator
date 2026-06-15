# Skill: Knowledge Base Structuring

## Objective
Convert the refined article into a structured knowledge base article.

## Required Sections
1. Title
2. Overview
3. Step 1, Step 2, Step 3, ...
4. Notes
5. Summary

## JSON Output Schema
Return valid JSON only with this structure:
```json
{
  "title": "string",
  "overview": "string",
  "steps": [
    {
      "step_number": 1,
      "heading": "string",
      "details": ["string", "string"]
    }
  ],
  "notes": ["string"],
  "summary": "string"
}
```
