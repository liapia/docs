# Design Twitter/X Bot

Posts design tips, quotes, resources, loved links, and retweets to X.
Optionally attaches images from `media/` automatically.

## Quick start

```bash
cd design-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in TWITTER_* keys (Read and Write)
```

## Commands

```bash
python generate_queue.py --replace   # rebuild queue
python bot.py --status               # inspect next item
python bot.py --dry-run              # preview (no API write)
python bot.py                        # publish next item
```

## What it posts

| Type | Source |
| --- | --- |
| Tips / quotes / trends | `content.py` |
| Link shares | `loves.py` → `LOVED_LINKS` |
| Retweets | `loves.py` → `LOVED_RETWEETS` |
| Images (auto) | files in `media/` |

No hashtags. No Steve Jobs quotes.

## Add things you love

Edit `loves.py`:

```python
LOVED_LINKS = [
    {"text": "Why this is great.", "url": "https://example.com"},
]

LOVED_RETWEETS = [
    "https://x.com/someone/status/1234567890123456789",
]
```

Then rebuild:

```bash
python generate_queue.py --replace
```

## Preview images (automatic)

Posts get images in this order:

1. **Manual** — drop files into `media/` (used first)
2. **Link previews** — Open Graph images fetched from URLs in the post
3. **Text cards** — generated cards for tips / quotes / trends when no OG image exists

Rebuild after changes:

```bash
python generate_queue.py --replace
python bot.py --dry-run   # shows [image] path when paired
```

## Files

| File | Purpose |
| --- | --- |
| `bot.py` | Status, dry-run, tweet + retweet + media upload |
| `generate_queue.py` | Builds the queue |
| `loves.py` | Your links + retweet list |
| `content.py` | Tips, quotes, resources, trends |
| `media/` | Images for auto-pairing |
| `.env` | API credentials (never commit) |
