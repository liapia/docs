# Design Twitter/X Bot

Posts design tips, quotes, resources, and trends to X from a local queue.

## Quick start (local venv)

```bash
cd design-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in TWITTER_* keys from https://console.x.com (Read and Write access)
```

## Commands

```bash
# Build / refill the post queue
python generate_queue.py

# Inspect the queue
python bot.py --status

# Preview the next post (no API call)
python bot.py --dry-run

# Post the next queue item to @leiroc_lia
python bot.py
```

## Files

| File | Purpose |
| --- | --- |
| `bot.py` | Status, dry-run, and live posting |
| `generate_queue.py` | Builds `data/queue.json` + `picks.md` |
| `queue_file.py` | Queue persistence |
| `sources.py` | Category wiring |
| `content.py` | Curated design copy |
| `.env` | Live API credentials (never commit) |

## X API setup

1. Open [console.x.com](https://console.x.com)
2. Use your **Default / Pay Per Use** project app
3. Set app permissions to **Read and Write**
4. On **Keys & Tokens**, copy:
   - Consumer Key → `TWITTER_API_KEY`
   - Consumer Secret → `TWITTER_API_SECRET`
   - Access Token → `TWITTER_ACCESS_TOKEN`
   - Access Token Secret → `TWITTER_ACCESS_TOKEN_SECRET`
5. Regenerate the Access Token after changing permissions so it says **Read and Write**

## Cloud Agent notes

Dependencies install into `design-bot/.venv` via the environment `install` script.
Add the four `TWITTER_*` values as Cloud Agent secrets (or a local `.env`) before live posting.
