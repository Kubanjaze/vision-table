# Phase 61 — Vision: Read Activity Table from Paper Image

**Version:** 1.1 | **Tier:** Standard | **Date:** 2026-03-26

## Goal
Demonstrate Claude's vision capability by extracting compound activity data from a table image.

CLI: `python main.py --image data/activity_table.png`

## Key Concepts
- Image content block: `{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "..."}}`
- Vision works with standard `client.messages.create()` — no special API needed
- Image + text prompt in same message content array

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
