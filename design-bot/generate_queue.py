"""Generate a shuffled queue of design posts ready to publish."""

from __future__ import annotations

import argparse
import random
import uuid
from datetime import datetime, timezone

from media_util import available_images, to_rel
from queue_file import QueueItem, load_queue, pending_items, save_queue
from sources import CATEGORIES, loved_link_posts, loved_retweet_ids

# Categories that benefit from an auto-attached image when media/ has files.
IMAGE_FRIENDLY = {"tip", "trend", "resource", "link"}


def _build_post(category: str, body: str) -> str:
    if category == "link":
        post = body
    else:
        label, _ = CATEGORIES[category]
        post = f"{label}:\n\n{body}"
    if len(post) > 280:
        post = body
    if len(post) > 280:
        post = body[:277] + "..."
    return post


def _used_image_paths(items: list[QueueItem]) -> set[str]:
    used: set[str] = set()
    for item in items:
        if item.image_path:
            used.add(item.image_path)
    return used


def generate_queue(count: int = 24, replace: bool = False) -> list[QueueItem]:
    existing = [] if replace else load_queue()
    posted = [item for item in existing if item.posted_at is not None]
    keep_pending = [] if replace else pending_items(existing)

    pool: list[tuple[str, str, str | None]] = []
    # (category, text_or_empty, retweet_id)

    for key, (_label, entries) in CATEGORIES.items():
        for entry in entries:
            pool.append((key, entry, None))

    for link_post in loved_link_posts():
        pool.append(("link", link_post, None))

    for tweet_id in loved_retweet_ids():
        pool.append(("retweet", "", tweet_id))

    random.shuffle(pool)
    needed = max(0, count - len(keep_pending))
    created: list[QueueItem] = []
    now = datetime.now(timezone.utc).isoformat()

    used_images = _used_image_paths(posted + keep_pending)
    image_queue = available_images(used_images)

    for category, body, retweet_id in pool:
        if len(created) >= needed:
            break

        text = "" if category == "retweet" else _build_post(category, body)
        image_path = None
        if category in IMAGE_FRIENDLY and image_queue:
            image_path = to_rel(image_queue.pop(0))
            used_images.add(image_path)

        if category == "retweet":
            text = f"Retweet {retweet_id}"

        created.append(
            QueueItem(
                id=str(uuid.uuid4())[:8],
                text=text,
                category=category,
                created_at=now,
                image_path=image_path,
                retweet_id=retweet_id,
            )
        )

    items = posted + keep_pending + created
    # Interleave a bit so retweets/links aren't all clustered at the end
    # of a refill — keep already-pending order, only shuffle new slice.
    save_queue(items)
    return items


def write_picks_preview(items: list[QueueItem], path: str = "picks.md") -> None:
    pending = pending_items(items)
    lines = [
        "# Design bot queue",
        "",
        f"Pending: **{len(pending)}** · Total: **{len(items)}**",
        "",
    ]
    for index, item in enumerate(pending, start=1):
        meta = [item.category]
        if item.image_path:
            meta.append(f"image: {item.image_path}")
        if item.retweet_id:
            meta.append(f"rt: {item.retweet_id}")
        lines.extend(
            [
                f"## {index}. `{item.id}` · {' · '.join(meta)}",
                "",
                "```",
                item.text or "(retweet only)",
                "```",
                "",
            ]
        )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a design post queue")
    parser.add_argument("--count", type=int, default=24, help="Target pending posts")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Drop unposted items and rebuild the pending queue",
    )
    args = parser.parse_args()

    items = generate_queue(count=args.count, replace=args.replace)
    write_picks_preview(items)
    pending = pending_items(items)
    with_images = sum(1 for item in pending if item.image_path)
    retweets = sum(1 for item in pending if item.retweet_id)
    print(
        f"Queue ready: {len(pending)} pending / {len(items)} total "
        f"({with_images} with images, {retweets} retweets)"
    )
    print("Preview written to picks.md")
    if pending:
        nxt = pending[0]
        print("\nNext up:\n")
        print(nxt.text or f"(retweet {nxt.retweet_id})")
        if nxt.image_path:
            print(f"\n[image] {nxt.image_path}")


if __name__ == "__main__":
    main()
