import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import argparse, os, json, base64, re, warnings
warnings.filterwarnings("ignore")
from dotenv import load_dotenv
import anthropic

load_dotenv()
os.environ.setdefault("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY", ""))

# Ground truth for the first 8 compounds
GROUND_TRUTH = {
    "benz_001_F": 7.25, "benz_002_Cl": 7.65, "benz_003_Br": 7.55, "benz_004_CF3": 8.10,
    "benz_005_CN": 7.95, "benz_006_NO2": 7.45, "benz_007_Me": 6.60, "benz_008_OMe": 6.35,
}


def load_image_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--image", required=True, help="Path to activity table PNG")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # Local validation
    if not os.path.exists(args.image):
        print(f"ERROR: Image not found: {args.image}")
        return
    img_b64 = load_image_base64(args.image)
    print(f"\nPhase 61 — Vision: Activity Table Extraction")
    print(f"Image: {args.image} ({len(img_b64)//1024} KB base64)")
    print(f"Model: {args.model}\n")

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=args.model,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": img_b64}
                },
                {
                    "type": "text",
                    "text": (
                        "Extract ALL rows from this activity data table. "
                        "Return a JSON array of objects with fields: compound_name, smiles, pic50 (float). "
                        "Respond ONLY with the JSON array, no other text."
                    )
                }
            ]
        }]
    )

    text = ""
    for block in response.content:
        if hasattr(block, "text"):
            text = block.text
            break

    print(f"Raw response:\n{text[:500]}\n")

    # Parse JSON array
    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    records = []
    if json_match:
        try:
            records = json.loads(json_match.group())
        except Exception as e:
            print(f"JSON parse error: {e}")

    # Validate against ground truth
    n_name_ok = 0
    n_pic50_ok = 0
    for rec in records:
        name = rec.get("compound_name", "")
        pic50 = rec.get("pic50", 0)
        gt_pic50 = GROUND_TRUTH.get(name)
        name_ok = name in GROUND_TRUTH
        pic50_ok = gt_pic50 is not None and abs(pic50 - gt_pic50) < 0.05
        if name_ok: n_name_ok += 1
        if pic50_ok: n_pic50_ok += 1
        tag = "OK" if (name_ok and pic50_ok) else "MISS"
        print(f"  {name:20s} pIC50={pic50:5.2f} (gt={gt_pic50 or '?':>5}) [{tag}]")

    usage = response.usage
    cost = (usage.input_tokens / 1e6 * 0.80) + (usage.output_tokens / 1e6 * 4.0)

    report = (
        f"Phase 61 — Vision: Activity Table Extraction\n"
        f"{'='*50}\n"
        f"Model:          {args.model}\n"
        f"Records extracted: {len(records)}\n"
        f"Name accuracy:  {n_name_ok}/{len(records)}\n"
        f"pIC50 accuracy: {n_pic50_ok}/{len(records)}\n"
        f"Input tokens:   {usage.input_tokens}\n"
        f"Output tokens:  {usage.output_tokens}\n"
        f"Est. cost:      ${cost:.4f}\n"
    )
    print(f"\n{report}")

    with open(os.path.join(args.output_dir, "extracted_data.json"), "w") as f:
        json.dump(records, f, indent=2)
    with open(os.path.join(args.output_dir, "vision_report.txt"), "w") as f:
        f.write(report)
    print(f"Saved: {args.output_dir}/extracted_data.json")
    print(f"Saved: {args.output_dir}/vision_report.txt")
    print("\nDone.")


if __name__ == "__main__":
    main()
