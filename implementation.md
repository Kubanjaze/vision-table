# Phase 61 — Vision: Read Activity Table from Paper Image

**Version:** 1.1 | **Tier:** Standard | **Date:** 2026-03-26

## Goal
Demonstrate Claude's vision capability by extracting compound activity data from a table image.

CLI: `python main.py --image data/activity_table.png`

## Logic
- Generate a table image from compounds.csv using matplotlib (make_table_image.py)
- Load PNG, encode as base64 string
- Send to Claude as image content block + text prompt asking for JSON extraction
- Parse JSON array from response, compare against ground truth (8 compounds)
- Score: exact match on compound_name, SMILES; ±0.05 on pIC50

## Key Concepts
- Image content block: `{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "..."}}`
- Vision works with standard `client.messages.create()` — no special API needed
- Image + text prompt in same message content array

## Verification Checklist
- [x] Image loaded and base64-encoded correctly
- [x] Claude extracts all 8 compound names correctly
- [x] All 8 pIC50 values match ground truth exactly
- [x] SMILES extracted (validated by presence, not canonicalization)
- [x] One clean API call

## Risks (resolved)
- Long SMILES strings may be partially misread from image — not observed (all correct)
- Image resolution affects extraction — 150 DPI was sufficient
- Matplotlib table formatting may obscure cell borders — clean extraction achieved

## Results
| Metric | Value |
|--------|-------|
| Records extracted | 8/8 |
| Name accuracy | 8/8 (100%) |
| pIC50 accuracy | 8/8 (100%) |
| Input tokens | 615 |
| Output tokens | 482 |
| Est. cost | $0.0024 |

Perfect extraction: all compound names, SMILES, and pIC50 values matched ground truth exactly.
One clean API call — no debug iterations needed.
