"""Auto image helpers for the design bot."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEDIA_DIR = ROOT / "media"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def list_images() -> list[Path]:
    if not MEDIA_DIR.exists():
        return []
    images = [
        path
        for path in sorted(MEDIA_DIR.iterdir())
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return images


def available_images(used_paths: set[str]) -> list[Path]:
    unused = []
    for path in list_images():
        rel = str(path.relative_to(ROOT))
        if rel not in used_paths and path.name not in used_paths:
            unused.append(path)
    return unused


def to_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)
