"""Generate simple text preview cards for tip/quote/trend posts."""

from __future__ import annotations

import hashlib
import logging
import textwrap
from pathlib import Path

from media_util import MEDIA_DIR, to_rel

log = logging.getLogger("design-bot")

CACHE_DIR = MEDIA_DIR / "cards"


def _font(size: int):
    from PIL import ImageFont

    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def generate_text_card(text: str, category: str) -> str | None:
    """Render a clean 1200x675 card. Returns repo-relative path."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        log.warning("Pillow not installed — skipping text cards")
        return None

    body = (text or "").strip()
    if not body:
        return None

    # Drop label prefix lines like "💡 Design tip:" for cleaner cards.
    lines = [line for line in body.splitlines() if line.strip()]
    if lines and lines[0].endswith(":") and len(lines) > 1:
        lines = lines[1:]
    body = "\n".join(lines).strip()
    if not body:
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(f"{category}:{body}".encode("utf-8")).hexdigest()[:16]
    dest = CACHE_DIR / f"{digest}.png"
    if dest.exists():
        return to_rel(dest)

    width, height = 1200, 675
    # Cool paper + charcoal — avoid generic purple / cream-terracotta defaults.
    bg = (242, 244, 246)
    ink = (22, 24, 28)
    mute = (100, 108, 116)
    accent = (15, 118, 110)

    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image)
    title_font = _font(28)
    body_font = _font(42)
    foot_font = _font(22)

    label = {
        "tip": "DESIGN TIP",
        "quote": "DESIGN WISDOM",
        "trend": "DESIGN TREND",
        "resource": "DESIGN RESOURCE",
    }.get(category, "DESIGN")

    draw.rectangle((0, 0, 18, height), fill=accent)
    draw.text((64, 56), label, fill=mute, font=title_font)

    wrapped = textwrap.fill(body, width=34)
    draw.multiline_text((64, 140), wrapped, fill=ink, font=body_font, spacing=12)
    draw.text((64, height - 72), "@leiroc_lia", fill=mute, font=foot_font)

    image.save(dest, format="PNG", optimize=True)
    log.info("Generated card %s", dest.name)
    return to_rel(dest)
