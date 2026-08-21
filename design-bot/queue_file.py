"""Persistent post queue stored as JSON."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
QUEUE_PATH = DATA_DIR / "queue.json"


@dataclass
class QueueItem:
    id: str
    text: str
    category: str
    created_at: str
    posted_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "QueueItem":
        return cls(
            id=data["id"],
            text=data["text"],
            category=data["category"],
            created_at=data["created_at"],
            posted_at=data.get("posted_at"),
        )


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_queue() -> list[QueueItem]:
    if not QUEUE_PATH.exists():
        return []
    raw = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    return [QueueItem.from_dict(item) for item in raw.get("items", [])]


def save_queue(items: list[QueueItem]) -> None:
    _ensure_data_dir()
    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "items": [asdict(item) for item in items],
    }
    QUEUE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def pending_items(items: list[QueueItem] | None = None) -> list[QueueItem]:
    items = items if items is not None else load_queue()
    return [item for item in items if item.posted_at is None]


def mark_posted(item_id: str) -> QueueItem | None:
    items = load_queue()
    for item in items:
        if item.id == item_id:
            item.posted_at = datetime.now(timezone.utc).isoformat()
            save_queue(items)
            return item
    return None


def queue_exists() -> bool:
    return QUEUE_PATH.exists()
