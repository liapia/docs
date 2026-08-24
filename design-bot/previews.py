"""Fetch link preview images (Open Graph) and cache them locally."""

from __future__ import annotations

import hashlib
import logging
import re
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

from media_util import MEDIA_DIR, to_rel

log = logging.getLogger("design-bot")

ROOT = Path(__file__).resolve().parent
CACHE_DIR = MEDIA_DIR / "cache"
URL_RE = re.compile(r"https?://[^\s<>\"']+")
OG_RE = re.compile(
    r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
OG_RE_ALT = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\'](?:og:image|twitter:image(?::src)?)["\']',
    re.I,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; DesignBot/1.0; +https://x.com/leiroc_lia) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,image/*,*/*;q=0.8",
}


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    return URL_RE.findall(text)


def _slug(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def _find_og_image(html: str, page_url: str) -> str | None:
    match = OG_RE.search(html) or OG_RE_ALT.search(html)
    if not match:
        return None
    raw = unescape(match.group(1).strip())
    if not raw or raw.startswith("data:"):
        return None
    return urljoin(page_url, raw)


def _extension_from(url: str, content_type: str | None) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    if content_type:
        if "png" in content_type:
            return ".png"
        if "webp" in content_type:
            return ".webp"
        if "gif" in content_type:
            return ".gif"
    return ".jpg"


def fetch_og_preview(page_url: str) -> str | None:
    """Download og:image for a page into media/cache/. Returns repo-relative path."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    existing = list(CACHE_DIR.glob(f"{_slug(page_url)}.*"))
    if existing:
        return to_rel(existing[0])

    try:
        page = requests.get(page_url, headers=HEADERS, timeout=20, allow_redirects=True)
        page.raise_for_status()
    except requests.RequestException as exc:
        log.warning("Preview page fetch failed for %s: %s", page_url, exc)
        return None

    image_url = _find_og_image(page.text, page.url)
    if not image_url:
        log.warning("No og:image found for %s", page_url)
        return None

    try:
        image = requests.get(image_url, headers=HEADERS, timeout=30, allow_redirects=True)
        image.raise_for_status()
    except requests.RequestException as exc:
        log.warning("Preview image download failed for %s: %s", image_url, exc)
        return None

    content_type = (image.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    if content_type and not content_type.startswith("image/"):
        log.warning("Preview URL was not an image (%s): %s", content_type, image_url)
        return None

    ext = _extension_from(image_url, content_type)
    dest = CACHE_DIR / f"{_slug(page_url)}{ext}"
    dest.write_bytes(image.content)
    if dest.stat().st_size < 1024:
        dest.unlink(missing_ok=True)
        log.warning("Preview image too small, skipped: %s", image_url)
        return None

    log.info("Cached preview for %s -> %s", page_url, dest.name)
    return to_rel(dest)


def resolve_link_preview(text: str) -> str | None:
    urls = extract_urls(text)
    if not urls:
        return None
    # Prefer the last URL (usually the shared link).
    return fetch_og_preview(urls[-1])
