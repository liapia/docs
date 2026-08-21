"""Sources used when building the post queue."""

from __future__ import annotations

import re

from content import (
    DESIGN_QUOTES,
    DESIGN_RESOURCES,
    DESIGN_TIPS,
    DESIGN_TRENDS,
)
from loves import LOVED_LINKS, LOVED_RETWEETS

CATEGORIES = {
    "tip": ("💡 Design tip", DESIGN_TIPS),
    "quote": ("✨ Design wisdom", DESIGN_QUOTES),
    "resource": ("🔗 Design resource", DESIGN_RESOURCES),
    "trend": ("📈 Design trend", DESIGN_TRENDS),
}

STATUS_ID_RE = re.compile(r"(?:status(?:es)?/)(\d{5,})")


def parse_tweet_id(value: str) -> str | None:
    value = (value or "").strip()
    if not value:
        return None
    if value.isdigit():
        return value
    match = STATUS_ID_RE.search(value)
    return match.group(1) if match else None


def loved_link_posts() -> list[str]:
    posts = []
    for item in LOVED_LINKS:
        text = (item.get("text") or "").strip()
        url = (item.get("url") or "").strip()
        if not text or not url:
            continue
        post = f"{text}\n{url}"
        if len(post) > 280:
            # Prefer keeping the URL; trim the prose.
            room = 280 - len(url) - 1
            if room < 20:
                post = url
            else:
                post = f"{text[: room - 1].rstrip()}…\n{url}"
        posts.append(post)
    return posts


def loved_retweet_ids() -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for value in LOVED_RETWEETS:
        tweet_id = parse_tweet_id(value)
        if tweet_id and tweet_id not in seen:
            seen.add(tweet_id)
            ids.append(tweet_id)
    return ids


__all__ = [
    "CATEGORIES",
    "loved_link_posts",
    "loved_retweet_ids",
    "parse_tweet_id",
]
