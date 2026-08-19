# Design Twitter/X Bot

An automated bot that posts design tips, quotes, resources, and trends to Twitter/X.

## What it posts

- **Design tips** — practical advice on typography, color, layout, spacing, and more
- **Design quotes** — wisdom from legendary designers
- **Design resources** — tools, books, fonts, and websites worth checking out
- **Design trends** — what's happening in the design world right now

Posts are randomly generated from a curated content library and tagged with relevant hashtags.

## Setup

### 1. Get Twitter/X API credentials

1. Go to the [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. Create a project and app
3. Generate API Key, API Secret, Access Token, and Access Token Secret
4. Make sure your app has **Read and Write** permissions

### 2. Configure the bot

```bash
cd design-bot
cp .env.example .env
# Edit .env with your API credentials
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Post a single tweet

```bash
python bot.py
```

### Preview without posting (dry run)

```bash
python bot.py --dry-run
```

### Run on a schedule

```bash
python bot.py --schedule
```

Posts every 6 hours by default. Change `POST_INTERVAL_HOURS` in `.env` to adjust.

### Run with cron (alternative)

Add to your crontab to post every 6 hours:

```
0 */6 * * * cd /path/to/design-bot && python bot.py
```

## Customizing content

Edit `content.py` to add your own tips, quotes, resources, and trends. Each category is a simple Python list — just append new strings.

## File structure

```
design-bot/
├── bot.py              # Main bot logic and CLI
├── content.py          # Curated design content library
├── requirements.txt    # Python dependencies
├── .env.example        # Template for API credentials
└── README.md           # This file
```
