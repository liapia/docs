"""Things Lia loves — links to share and tweets to retweet.

Edit this file anytime. Rebuild the queue after changes:
  python generate_queue.py --replace
"""

from __future__ import annotations

# Short posts that share a link. Keep text short enough for X + URL.
LOVED_LINKS = [
    {
        "text": "One Page Love — still the best rabbit hole for landing-page craft.",
        "url": "https://onepagelove.com",
    },
    {
        "text": "Refero is where I go when I need real product UI references, not moodboards.",
        "url": "https://refero.design",
    },
    {
        "text": "Mobbin for mobile patterns that actually shipped.",
        "url": "https://mobbin.com",
    },
    {
        "text": "Phosphor Icons — clean, consistent, and free for product work.",
        "url": "https://phosphoricons.com",
    },
    {
        "text": "The Component Gallery — studying component anatomy across design systems.",
        "url": "https://component.gallery",
    },
    {
        "text": "Layers.to for portfolio / case-study inspiration.",
        "url": "https://www.layers.to",
    },
    {
        "text": "Godly — websites that feel designed, not templated.",
        "url": "https://godly.website",
    },
    {
        "text": "Fontpair when you need a type pairing that just works.",
        "url": "https://www.fontpair.co",
    },
    {
        "text": "Humaaans for quick, friendly people illustrations in product mocks.",
        "url": "https://www.humaaans.com",
    },
    {
        "text": "Sidebar — a weekly design/tech roundup worth actually opening.",
        "url": "https://sidebar.io",
    },
    {
        "text": "Law of UX — bite-size psychology principles for interface decisions.",
        "url": "https://lawsofux.com",
    },
    {
        "text": "Checklist Design — pre-ship UX checklists so nothing obvious slips.",
        "url": "https://www.checklist.design",
    },
]

# Paste full tweet URLs (or bare status IDs) you want the bot to retweet.
# Example: "https://x.com/someone/status/1234567890123456789"
LOVED_RETWEETS: list[str] = [
    # Add your favorites here ↓
]
