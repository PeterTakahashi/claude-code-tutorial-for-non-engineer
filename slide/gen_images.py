#!/usr/bin/env python3
"""Generate slide illustration images via Gemini (nano-banana) Batch API.

- Reads GEMINI_API_KEY from ../.env (project root) or env.
- Submits all images as ONE batch job (≈50% cheaper than per-image calls).
- Polls until done, then saves PNGs into slide/img/<key>.png.
- If the batch endpoint rejects the request, falls back to synchronous
  per-image generateContent so we still get images.
- Idempotent: skips keys whose PNG already exists (use --force to redo).

Stdlib only (urllib) — no pip installs needed. Run:
    python3 slide/gen_images.py
    python3 slide/gen_images.py --force
    python3 slide/gen_images.py --sync     # skip batch, generate one by one
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
API_ROOT = "https://generativelanguage.googleapis.com/v1beta"

HERE = Path(__file__).resolve().parent          # slide/
ROOT = HERE.parent                              # project root
OUT_DIR = HERE / "img"

STYLE = (
    "Warm, friendly, minimalist flat illustration for a beginner programming "
    "workshop slide. Solid warm cream background (hex #FAF9F6) filling the whole "
    "frame. Limited palette: warm terracotta-clay (#D97757) and teal-green "
    "(#2A9D8F) accents with soft charcoal (#1F2933) outlines. Simple rounded "
    "shapes, cute and approachable, clear and uncluttered, lots of negative "
    "space, gentle soft shadows. Made for non-engineers. Square 1:1 composition. "
    "ABSOLUTELY NO text, no letters, no numbers, no words, no captions, no "
    "labels, no UI writing anywhere in the image. Scene: "
)

SCENES: dict[str, str] = {
    "llm": (
        "a friendly smart assistant character with a calm, approachable smile, "
        "surrounded by many floating open books and paper documents, as if it "
        "has read everything and is ready to help answer questions."
    ),
    "restaurant": (
        "a clean side cross-section of one small cozy restaurant divided into "
        "four clearly separated zones placed left to right: (1) a dining area "
        "with a little table, a chair and a standing menu board; (2) a smiling "
        "waiter in an apron carrying a serving tray; (3) an open kitchen with a "
        "chef cooking at a stove with a pot; (4) a pantry storage room with "
        "shelves full of ingredient jars and boxes. Everything visible at a "
        "glance, cute and tidy."
    ),
    "docker": (
        "a neat sealed shipping box / container shown slightly open to reveal a "
        "ready-to-run program packed inside: a small database cylinder icon and "
        "a gear wheel, with a friendly glowing round power button on the front "
        "of the box. The idea of a program that comes pre-packed in a box that "
        "you just switch on, with no messy installation. Absolutely no kitchen, "
        "no cooking, no food, no stove."
    ),
    "remote_control": (
        "a person standing outdoors holding up a smartphone, sending a curved "
        "dotted wireless signal across to a desktop computer at home that is "
        "happily working by itself — the idea of controlling your PC from your "
        "phone while away."
    ),
    "mcp": (
        "a friendly rounded robot assistant with several USB-style connector "
        "ports along its body; short cables plug from those ports into three "
        "small floating icons: a globe (web browser), an envelope (email), and "
        "a calendar — the idea of plugging external tools into an AI."
    ),
    "skills": (
        "a friendly rounded robot holding an open ring-binder recipe book with "
        "colorful tabbed sections and small step-by-step pictograms on the "
        "pages; a couple of blank instruction cards float nearby — the idea of "
        "reusable how-to instruction packs."
    ),
    "agentic_loop": (
        "a big circular arrow loop forming a cycle, with four small pictogram "
        "stages spaced evenly around the ring: a glowing lightbulb (think), a "
        "hand placing a block (do), a magnifying glass over a checkmark "
        "(check), and a wrench (fix); a small friendly robot stands in the "
        "center of the loop."
    ),
    "playwright_robot": (
        "a cute rounded robot sitting at a desk operating a computer by itself, "
        "its hands on a keyboard and mouse, a web browser window open on the "
        "screen showing a simple map and a list, as if the robot is browsing "
        "and collecting information automatically."
    ),
    "test_rehearsal": (
        "a split scene with two halves: the left half shows a chef tasting a "
        "small spoonful from a pot (a single quick taste check); the right half "
        "shows a staff member pretending to be a customer walking through a "
        "full dining experience from entering to being served (a full "
        "rehearsal from start to finish)."
    ),
    "ngrok_tunnel": (
        "a small cozy house with a single glowing pipe-like tunnel extending "
        "out from it across a gap to a faraway friend holding a smartphone; the "
        "tunnel is the one temporary public road that lets the friend reach the "
        "house."
    ),
}


def load_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY"):
                _, _, val = line.partition("=")
                return val.strip().strip('"').strip("'")
    raise SystemExit("GEMINI_API_KEY not found (env or .env)")


API_KEY = load_api_key()


def _post(url: str, body: dict, timeout: float = 300.0) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json", "X-goog-api-key": API_KEY},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url: str, timeout: float = 120.0) -> dict:
    req = urllib.request.Request(
        url, method="GET", headers={"X-goog-api-key": API_KEY},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _write_first_image(parts: list[dict], out_path: Path) -> bool:
    for p in parts:
        inline = p.get("inlineData") or p.get("inline_data")
        if inline and inline.get("data"):
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(base64.b64decode(inline["data"]))
            return True
    return False


def gen_one(key: str, prompt: str, attempts: int = 8) -> bool:
    """Synchronous single-image generation with patient RPM backoff."""
    out_path = OUT_DIR / f"{key}.png"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    url = f"{API_BASE}/{MODEL}:generateContent"
    for attempt in range(1, attempts + 1):
        try:
            data = _post(url, body, timeout=180.0)
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "ignore")[:300]
            if e.code == 429 and attempt < attempts:
                wait = min(75.0, 30.0 + 8.0 * attempt)  # ride out the per-minute window
                print(f"  [{key}] 429 (RPM), waiting {wait:.0f}s ({attempt}/{attempts})")
                time.sleep(wait)
                continue
            print(f"  [{key}] HTTP {e.code}: {txt}")
            return False
        parts: list[dict] = []
        for c in data.get("candidates", []):
            parts.extend(c.get("content", {}).get("parts", []))
        if _write_first_image(parts, out_path):
            print(f"  [{key}] ok → {out_path.name}")
            return True
        print(f"  [{key}] empty response, retry {attempt}/{attempts}")
        time.sleep(6)
    return False


def gen_batch(jobs: list[tuple[str, str]], poll_interval_s: float = 30.0,
              max_wait_s: float = 7200.0) -> tuple[list[str], list[str]]:
    """Submit all jobs as one batch. Returns (done_keys, failed_keys).

    Raises on submit failure so the caller can fall back to sync.
    """
    inlined = []
    for i, (key, prompt) in enumerate(jobs):
        inlined.append({
            "request": {"contents": [{"parts": [{"text": prompt}]}]},
            "metadata": {"key": key},
        })
    body = {
        "batch": {
            "display_name": "slide-illustrations",
            "input_config": {"requests": {"requests": inlined}},
        }
    }
    submit_url = f"{API_BASE}/{MODEL}:batchGenerateContent"
    print(f"→ submitting batch ({len(jobs)} images) to {MODEL} …")
    op = _post(submit_url, body)
    batch_name = op.get("name")
    if not batch_name:
        raise RuntimeError(f"no batch name in response: {op}")
    print(f"  batch submitted: {batch_name}")

    poll_url = f"{API_ROOT}/{batch_name}"
    deadline = time.time() + max_wait_s
    last_state = None
    status: dict = {}
    while True:
        if time.time() > deadline:
            raise TimeoutError(f"batch not finished within {max_wait_s:.0f}s")
        time.sleep(poll_interval_s)
        try:
            status = _get(poll_url)
        except urllib.error.HTTPError as e:
            print(f"  poll HTTP {e.code} — retrying")
            continue
        md = status.get("metadata") or {}
        state = md.get("state") or status.get("state")
        done = status.get("done", False)
        if state != last_state:
            print(f"  batch state: {state}{' (done)' if done else ''}")
            last_state = state
        if state in {"JOB_STATE_SUCCEEDED", "BATCH_STATE_SUCCEEDED"} or done:
            break
        if state in {"JOB_STATE_FAILED", "BATCH_STATE_FAILED",
                     "JOB_STATE_CANCELLED", "BATCH_STATE_CANCELLED"}:
            raise RuntimeError(f"batch ended in {state}: {json.dumps(status)[:600]}")

    md = status.get("metadata") or {}
    response = status.get("response") or {}
    raw = (response.get("inlinedResponses")
           or response.get("dest", {}).get("inlinedResponses")
           or md.get("dest", {}).get("inlinedResponses"))
    if isinstance(raw, dict):
        items = raw.get("inlinedResponses") or next(
            (v for v in raw.values() if isinstance(v, list)), [])
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    if not items:
        (OUT_DIR / "_batch_status.json").write_text(json.dumps(status, indent=2))
        raise RuntimeError("batch succeeded but no inlinedResponses (dumped _batch_status.json)")

    done_keys: list[str] = []
    failed_keys: list[str] = []
    for i, item in enumerate(items):
        # map back to key via metadata.key, else positional
        key = (item.get("metadata") or {}).get("key") or jobs[i][0]
        out_path = OUT_DIR / f"{key}.png"
        if item.get("error"):
            print(f"  [{key}] error: {str(item['error'])[:200]}")
            failed_keys.append(key)
            continue
        resp = item.get("response") or {}
        parts: list[dict] = []
        for c in resp.get("candidates", []):
            parts.extend(c.get("content", {}).get("parts", []))
        if _write_first_image(parts, out_path):
            print(f"  [{key}] ok → {out_path.name}")
            done_keys.append(key)
        else:
            print(f"  [{key}] no image in response")
            failed_keys.append(key)
    return done_keys, failed_keys


def main() -> int:
    force = "--force" in sys.argv
    sync_only = "--sync" in sys.argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    jobs: list[tuple[str, str]] = []
    for key, scene in SCENES.items():
        out_path = OUT_DIR / f"{key}.png"
        if out_path.exists() and not force:
            print(f"  [{key}] exists, skip")
            continue
        jobs.append((key, STYLE + scene))

    if not jobs:
        print("All images already present. Use --force to regenerate.")
        return 0

    if not sync_only:
        try:
            done, failed = gen_batch(jobs)
            print(f"\nbatch done: {len(done)} ok, {len(failed)} failed")
            if failed:
                print(f"retrying {len(failed)} via sync …")
                for key in failed:
                    gen_one(key, STYLE + SCENES[key])
            return 0
        except Exception as e:  # noqa: BLE001
            print(f"\nbatch path failed ({e}); falling back to sync generation …")

    ok = 0
    for i, (key, prompt) in enumerate(jobs):
        if i:
            time.sleep(3)  # small spacing; gen_one() backs off if RPM is hit
        if gen_one(key, prompt):
            ok += 1
    print(f"\nsync done: {ok}/{len(jobs)} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
