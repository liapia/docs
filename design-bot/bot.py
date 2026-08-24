"""Design Twitter/X bot — posts the next item from a local queue."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from generate_queue import generate_queue, write_picks_preview
from queue_file import load_queue, mark_posted, pending_items, queue_exists, save_queue
from resolve_media import resolve_preview

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
    values = {key: (os.getenv(key) or "").strip().strip("<>") for key in required}
    missing = [key for key, value in values.items() if not value]
    if missing:
        log.error("Missing credentials in .env: %s", ", ".join(missing))
        log.error("Copy .env.example to .env and add your X API keys.")
        sys.exit(1)
    return values


def _clients():
    """Return (v2 Client, v1.1 API) — v1.1 is required for media upload."""
    import tweepy

    creds = _require_credentials()
    client = tweepy.Client(
        consumer_key=creds["TWITTER_API_KEY"],
        consumer_secret=creds["TWITTER_API_SECRET"],
        access_token=creds["TWITTER_ACCESS_TOKEN"],
        access_token_secret=creds["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    auth = tweepy.OAuth1UserHandler(
        creds["TWITTER_API_KEY"],
        creds["TWITTER_API_SECRET"],
        creds["TWITTER_ACCESS_TOKEN"],
        creds["TWITTER_ACCESS_TOKEN_SECRET"],
    )
    api = tweepy.API(auth)
    return client, api


def ensure_queue(min_pending: int = 5) -> None:
    if not queue_exists() or len(pending_items()) < min_pending:
        log.info("Generating queue...")
        items = generate_queue(count=max(24, min_pending))
        write_picks_preview(items, path=str(ROOT / "picks.md"))


def _describe(item) -> str:
    parts = [item.text or f"(retweet {item.retweet_id})"]
    if item.image_path:
        parts.append(f"[image] {item.image_path}")
    if item.retweet_id and item.category == "retweet":
        parts.append(f"[retweet] https://x.com/i/status/{item.retweet_id}")
    return "\n".join(parts)


def status() -> None:
    if not queue_exists():
        print("No queue file exists. Run: python generate_queue.py")
        return
    items = load_queue()
    pending = pending_items(items)
    posted = [item for item in items if item.posted_at]
    with_images = sum(1 for item in pending if item.image_path)
    retweets = sum(1 for item in pending if item.retweet_id)
    print(
        f"Queue: {len(pending)} pending · {len(posted)} posted · {len(items)} total "
        f"({with_images} images, {retweets} retweets)"
    )
    if pending:
        print("\nNext post:\n")
        print(_describe(pending[0]))
    else:
        print("Queue is empty. Run: python generate_queue.py")


def _upload_image(api, image_path: str) -> int:
    path = Path(image_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    media = api.media_upload(filename=str(path))
    return media.media_id


def post_next(*, dry_run: bool = False) -> str | None:
    ensure_queue()
    pending = pending_items()
    if not pending:
        log.error("No pending posts in the queue.")
        return None

    item = pending[0]

    # Ensure every non-retweet gets a preview image when possible.
    if not item.image_path and item.category != "retweet":
        try:
            preview = resolve_preview(item)
        except Exception:
            log.exception("Preview resolve failed for %s", item.id)
            preview = None
        if preview:
            item.image_path = preview
            items = load_queue()
            for queued in items:
                if queued.id == item.id:
                    queued.image_path = preview
                    break
            save_queue(items)

    log.info(
        "Selected %s (%s) chars=%d image=%s rt=%s",
        item.id,
        item.category,
        len(item.text or ""),
        item.image_path or "-",
        item.retweet_id or "-",
    )
    print(_describe(item))

    if dry_run:
        log.info("Dry run — nothing posted.")
        return item.text or item.retweet_id

    client, api = _clients()
    try:
        if item.category == "retweet" and item.retweet_id:
            client.retweet(item.retweet_id)
            url = f"https://x.com/i/status/{item.retweet_id}"
            mark_posted(item.id)
            write_picks_preview(load_queue(), path=str(ROOT / "picks.md"))
            log.info("Retweeted: %s", url)
            print(url)
            return url

        media_ids = None
        if item.image_path:
            media_id = _upload_image(api, item.image_path)
            media_ids = [media_id]
            log.info("Uploaded media_id=%s", media_id)

        response = client.create_tweet(text=item.text, media_ids=media_ids)
        tweet_id = response.data["id"]
        url = f"https://x.com/i/status/{tweet_id}"
        mark_posted(item.id)
        write_picks_preview(load_queue(), path=str(ROOT / "picks.md"))
        log.info("Posted: %s", url)
        print(url)
        return url
    except Exception:
        log.exception("Failed to publish queue item")
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
