"""Design Twitter/X bot — posts the next item from a local queue."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from generate_queue import generate_queue, write_picks_preview
from queue_file import load_queue, mark_posted, pending_items, queue_exists

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(ROOT / "bot.log"),
    ],
)
log = logging.getLogger("design-bot")


def _require_credentials() -> dict[str, str]:
    required = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
    ]
    values = {key: (os.getenv(key) or "").strip() for key in required}
    missing = [key for key, value in values.items() if not value]
    if missing:
        log.error("Missing credentials in .env: %s", ", ".join(missing))
        log.error("Copy .env.example to .env and add your X API keys.")
        sys.exit(1)
    return values


def _client():
    import tweepy

    creds = _require_credentials()
    return tweepy.Client(
        consumer_key=creds["TWITTER_API_KEY"],
        consumer_secret=creds["TWITTER_API_SECRET"],
        access_token=creds["TWITTER_ACCESS_TOKEN"],
        access_token_secret=creds["TWITTER_ACCESS_TOKEN_SECRET"],
    )


def ensure_queue(min_pending: int = 5) -> None:
    if not queue_exists() or len(pending_items()) < min_pending:
        log.info("Generating queue...")
        items = generate_queue(count=max(20, min_pending))
        write_picks_preview(items, path=str(ROOT / "picks.md"))


def status() -> None:
    if not queue_exists():
        print("No queue file exists. Run: python generate_queue.py")
        return
    items = load_queue()
    pending = pending_items(items)
    posted = [item for item in items if item.posted_at]
    print(f"Queue: {len(pending)} pending · {len(posted)} posted · {len(items)} total")
    if pending:
        print("\nNext post:\n")
        print(pending[0].text)
    else:
        print("Queue is empty. Run: python generate_queue.py")


def post_next(*, dry_run: bool = False) -> str | None:
    ensure_queue()
    pending = pending_items()
    if not pending:
        log.error("No pending posts in the queue.")
        return None

    item = pending[0]
    log.info("Selected %s (%s), %d chars", item.id, item.category, len(item.text))
    print(item.text)

    if dry_run:
        log.info("Dry run — nothing posted.")
        return item.text

    client = _client()
    try:
        response = client.create_tweet(text=item.text)
        tweet_id = response.data["id"]
        url = f"https://x.com/i/status/{tweet_id}"
        mark_posted(item.id)
        write_picks_preview(load_queue(), path=str(ROOT / "picks.md"))
        log.info("Posted: %s", url)
        print(url)
        return url
    except Exception:
        log.exception("Failed to post tweet")
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Design Twitter/X bot")
    parser.add_argument("--dry-run", action="store_true", help="Preview next post")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    args = parser.parse_args()

    if args.status:
        status()
        return

    post_next(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
