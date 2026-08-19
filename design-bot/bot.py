"""Twitter/X design bot — posts design tips, quotes, resources, and trends."""

import os
import sys
import logging
from datetime import datetime

import tweepy
from dotenv import load_dotenv

from content import get_random_post

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("bot.log")],
)
log = logging.getLogger(__name__)


def get_client() -> tweepy.Client:
    """Authenticate with the Twitter/X API v2."""
    required = [
        "TWITTER_API_KEY",
        "TWITTER_API_SECRET",
        "TWITTER_ACCESS_TOKEN",
        "TWITTER_ACCESS_TOKEN_SECRET",
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        log.error("Missing environment variables: %s", ", ".join(missing))
        log.error("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    return tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )


def post_tweet(dry_run: bool = False) -> str | None:
    """Generate and post a design tweet. Returns the tweet text."""
    text = get_random_post()
    log.info("Generated tweet (%d chars):\n%s", len(text), text)

    if dry_run:
        log.info("Dry run — tweet not posted.")
        return text

    client = get_client()
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        log.info("Posted tweet: https://x.com/i/status/%s", tweet_id)
        return text
    except tweepy.TweepyException:
        log.exception("Failed to post tweet")
        return None


def run_scheduler():
    """Run the bot on a repeating schedule."""
    import schedule
    import time

    interval = int(os.getenv("POST_INTERVAL_HOURS", "6"))
    log.info("Starting scheduler — posting every %d hours", interval)

    post_tweet()
    schedule.every(interval).hours.do(post_tweet)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Design Twitter/X Bot")
    parser.add_argument("--dry-run", action="store_true", help="Preview a tweet without posting")
    parser.add_argument("--schedule", action="store_true", help="Run on a repeating schedule")
    args = parser.parse_args()

    if args.dry_run:
        post_tweet(dry_run=True)
    elif args.schedule:
        run_scheduler()
    else:
        post_tweet()
