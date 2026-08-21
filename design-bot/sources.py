"""Sources used when building the post queue."""

from __future__ import annotations

from content import (
    DESIGN_QUOTES,
    DESIGN_RESOURCES,
    DESIGN_TIPS,
    DESIGN_TRENDS,
)

CATEGORIES = {
    "tip": ("💡 Design tip", DESIGN_TIPS),
    "quote": ("✨ Design wisdom", DESIGN_QUOTES),
    "resource": ("🔗 Design resource", DESIGN_RESOURCES),
    "trend": ("📈 Design trend", DESIGN_TRENDS),
}

__all__ = ["CATEGORIES"]
