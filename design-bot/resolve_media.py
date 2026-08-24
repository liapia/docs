"""Resolve the best preview image for a queue item."""

from __future__ import annotations

import logging

from cards import generate_text_card
from previews import resolve_link_preview
from queue_file import QueueItem

log = logging.getLogger("design-bot")


def resolve_preview(item: QueueItem) -> str | None:
    """Return a local image path for this item, or None."""
    if item.image_path:
        return item.image_path
    if item.category == "retweet":
        return None

    # 1) Open Graph preview for posts that include a URL
    preview = resolve_link_preview(item.text or "")
    if preview:
        return preview

    # 2) Generated text card for tip/quote/trend/resource without a usable OG image
    if item.category in {"tip", "quote", "trend", "resource"}:
        return generate_text_card(item.text or "", item.category)

    # 3) Link posts without OG still get a text card so they never go out blank
    if item.category == "link":
        return generate_text_card(item.text or "", "resource")

    return None
