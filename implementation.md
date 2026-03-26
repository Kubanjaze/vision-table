# Phase 61 — Vision: Read Activity Table from Paper Image

**Version:** 1.0 | **Tier:** Standard | **Date:** 2026-03-26

## Goal
Demonstrate Claude's vision capability by extracting compound activity data from a table image.
Send a PNG of an activity table, ask Claude to extract structured data, validate against ground truth.

CLI: `python main.py --image data/activity_table.png --n 8`

Outputs: extracted_data.json, vision_report.txt

## Logic
- Load a PNG image of an activity table (generated from compounds.csv)
- Encode image as base64 and send as image content block
- Ask Claude to extract compound_name, SMILES, pIC50 from the table
- Compare extracted values against ground truth CSV
- Report: extraction accuracy, field-level match rates

## Key Concepts
- Image content block: `{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "..."}}`
- Vision works with standard `client.messages.create()` — no special API
- Send image + text prompt in same message
- Parse JSON response into structured records

## Verification Checklist
- [ ] Image loaded and base64-encoded correctly
- [ ] Claude extracts compound names, SMILES, pIC50 values
- [ ] Accuracy reported vs ground truth

## Risks
- SMILES strings may be partially misread from image (long strings)
- pIC50 values should extract cleanly as they're short numbers
