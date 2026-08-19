"""Design content library for the Twitter/X bot."""

import random
from datetime import datetime

DESIGN_TIPS = [
    "White space isn't empty space — it's breathing room for your design. Use it generously.",
    "Limit your palette to 2–3 colors max. Constraints breed creativity.",
    "Typography is 90% of design. Pick one great typeface and learn it deeply.",
    "If everything is bold, nothing is bold. Create clear visual hierarchy.",
    "Design for the edges first — error states, empty states, loading states. The happy path is easy.",
    "Alignment is the invisible thread that holds a layout together. Snap to a grid.",
    "Contrast isn't just color — it's size, weight, spacing, and texture.",
    "Remove elements until your design breaks. Then add back only what's essential.",
    "The best icon is a text label. Use icons to reinforce meaning, not replace it.",
    "Rounded corners feel friendly. Sharp corners feel precise. Choose intentionally.",
    "Test your designs in grayscale. If the hierarchy works without color, it'll work with it.",
    "Consistency > creativity in UI. Save your creative energy for moments that matter.",
    "Good padding makes amateur work look professional instantly.",
    "Don't center-align body text. Left-align for readability, center-align for headlines only.",
    "Learn the 60-30-10 color rule: 60% dominant, 30% secondary, 10% accent.",
    "Optical alignment > mathematical alignment. Trust your eyes over the numbers.",
    "Design mobile-first, even if desktop is your primary target. It forces clarity.",
    "Group related elements. Proximity is the most underrated design principle.",
    "If you need to explain your design, it's not done yet.",
    "Steal like an artist — study great work, understand why it works, then make it yours.",
]

DESIGN_QUOTES = [
    '"Design is not just what it looks like and feels like. Design is how it works." — Steve Jobs',
    '"Good design is obvious. Great design is transparent." — Joe Sparano',
    '"Simplicity is the ultimate sophistication." — Leonardo da Vinci',
    '"Design is thinking made visual." — Saul Bass',
    '"Less, but better." — Dieter Rams',
    '"The details are not the details. They make the design." — Charles Eames',
    '"Design is intelligence made visible." — Alina Wheeler',
    '"Every great design begins with an even better story." — Lorinda Mamo',
    '"Design creates culture. Culture shapes values. Values determine the future." — Robert L. Peters',
    '"Whitespace is like air: it is necessary for design to breathe." — Wojciech Zieliński',
    '"A design isn\'t finished until someone is using it." — Brenda Laurel',
    '"The public is more familiar with bad design than good design." — Dieter Rams',
    '"Make it simple, but significant." — Don Draper',
    '"You can\'t use up creativity. The more you use, the more you have." — Maya Angelou',
    '"Color is a power which directly influences the soul." — Wassily Kandinsky',
]

DESIGN_RESOURCES = [
    "🎨 Tool of the day: Figma's auto layout — master it and your components will scale effortlessly.",
    "📚 Reading rec: 'Refactoring UI' by Adam Wathan & Steve Schoger. Practical design for developers.",
    "🔤 Font pairing tip: Inter + Fraunces. Clean sans-serif meets elegant serif.",
    "🎯 Try this: Mobbin.com — real-world mobile UI patterns from top apps.",
    "📐 Grid system tip: Use an 8px grid for spacing. Everything aligns, everything breathes.",
    "🖼️ Free illustrations: undraw.co — customizable SVG illustrations for any project.",
    "🌈 Color tool: coolors.co — generate beautiful palettes in seconds.",
    "📖 Reading rec: 'Don't Make Me Think' by Steve Krug. UX fundamentals that never go out of style.",
    "🧩 Component library worth studying: Radix UI — accessibility-first, composable primitives.",
    "✏️ Sketch exercise: redesign one screen of an app you use daily. Post your before/after.",
    "🎨 Color psychology: blue builds trust, red creates urgency, green signals growth.",
    "🔍 Contrast checker: webaim.org/resources/contrastchecker — accessibility isn't optional.",
    "📱 Responsive tip: test at 320px, 768px, and 1440px. Cover the extremes and the middle.",
    "💡 Inspiration: layers.to — curated design portfolios and case studies.",
    "🛠️ Prototyping tip: use Figma's smart animate for micro-interactions without code.",
]

DESIGN_TRENDS = [
    "Bento grid layouts are everywhere in 2026 — modular, flexible, and satisfying to look at.",
    "Glassmorphism is evolving: subtle frosted layers with higher contrast for better readability.",
    "Variable fonts are a game-changer — one file, infinite weights and widths.",
    "Dark mode isn't a trend, it's a standard. Design for both light and dark from the start.",
    "Micro-interactions are the new branding. A unique button animation says more than a logo.",
    "3D elements in flat UI — the sweet spot between skeuomorphism and minimalism.",
    "Hand-drawn illustrations are making a comeback, adding warmth to digital products.",
    "Neumorphism found its niche in dashboard design. Subtle depth, not the whole UI.",
    "Animated gradients as hero backgrounds — movement without distraction.",
    "Design systems aren't just for big teams anymore. Even solo designers benefit from tokens.",
]

HASHTAGS = [
    "#design", "#uidesign", "#uxdesign", "#designtips", "#webdesign",
    "#graphicdesign", "#productdesign", "#figma", "#typography",
    "#designinspiration", "#creativedirection", "#designthinking",
]


def get_random_post() -> str:
    """Generate a random design-related post with hashtags."""
    categories = [
        (DESIGN_TIPS, "💡 Design tip"),
        (DESIGN_QUOTES, "✨ Design wisdom"),
        (DESIGN_RESOURCES, "🔗 Design resource"),
        (DESIGN_TRENDS, "📈 Design trend"),
    ]

    category_list, label = random.choice(categories)
    content = random.choice(category_list)

    tags = random.sample(HASHTAGS, k=random.randint(2, 4))
    tag_str = " ".join(tags)

    day_name = datetime.now().strftime("%A")
    greeting = ""
    if day_name == "Monday":
        greeting = f"Happy {day_name}! "
    elif day_name == "Friday":
        greeting = "Happy Friday! "

    post = f"{greeting}{label}:\n\n{content}\n\n{tag_str}"

    if len(post) > 280:
        post = f"{content}\n\n{tag_str}"
    if len(post) > 280:
        post = content[:277] + "..."

    return post
