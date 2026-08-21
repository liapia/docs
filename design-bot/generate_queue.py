"""Generate a shuffled queue of design posts ready to publish."""

from __future__ import annotations

import argparse
import random
import uuid
from datetime import datetime, timezone

from queue_file import QueueItem, load_queue, pending_items, save_queue
from sources import CATEGORIES, HASHTAGS


def _build_post(category: str, body: str) -> str:
    label, _ = CATEGORIES[category]
    tags = " ".join(random.sample(HASHTAGS, k=random.randint(2, 3)))
    post = f"{label}:\n\n{body}\n\n{tags}"
    if len(post) > 280:
        post = f"{body}\n\n{tags}"
    if len(post) > 280:
        post = body[:277] + "..."
    return post


def generate_queue(count: int = 20, replace: bool = False) -> list[QueueItem]:
    existing = [] if replace else load_queue()
    posted = [item for item in existing if item.posted_at is not None]
    keep_pending = [] if replace else pending_items(existing)

    pool: list[tuple[str, str]] = []
    for key, (_label, entries) in CATEGORIES.items():
        for entry in entries:
            pool.append((key, entry))

    random.shuffle(pool)
    needed = max(0, count - len(keep_pending))
    created: list[QueueItem] = []
    now = datetime.now(timezone.utc).isoformat()

    for category, body in pool:
        if len(created) >= needed:
            break
        created.append(
            QueueItem(
                id=str(uuid.uuid4())[:8],
                text=_build_post(category, body),
                category=category,
                created_at=now,
            )
        )

    items = posted + keep_pending + created
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
        lines.extend(
            [
                f"## {index}. `{item.id}` · {item.category}",
                "",
                "```",
                item.text,
                "```",
                "",
            ]
        )
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a design post queue")
    parser.add_argument("--count", type=int, default=20, help="Target pending posts")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Drop unposted items and rebuild the pending queue",
    )
    args = parser.parse_args()

    items = generate_queue(count=args.count, replace=args.replace)
    write_picks_preview(items)
    pending = pending_items(items)
    print(f"Queue ready: {len(pending)} pending / {len(items)} total")
    print("Preview written to picks.md")
    if pending:
        print("\nNext up:\n")
        print(pending[0].text)


if __name__ == "__main__":
    main()
