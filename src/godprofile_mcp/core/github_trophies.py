"""GitHub trophy case SVG generator using stdlib only."""

from typing import Optional


def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


# Rank thresholds per trophy type: (S_min, A_min, B_min) — anything below B_min is C
_RANK_THRESHOLDS = {
    "Stars":     (1000, 200,  50),
    "Commits":   (3000, 1000, 300),
    "PRs":       (200,  50,   10),
    "Issues":    (200,  50,   10),
    "Repos":     (100,  30,   10),
    "Followers": (500,  100,  20),
}

_RANK_COLORS = {
    "S": "#ffd700",  # gold
    "A": "#c0c0c0",  # silver
    "B": "#cd7f32",  # bronze
    "C": None,       # falls back to theme text color
}

# SVG path for a simple trophy cup (scaled to ~40x50, centered at 0,0)
_TROPHY_CUP_PATH = (
    "M-16,-24 L16,-24 L20,-8 C20,4 12,12 4,14 L4,20 L10,20 L10,26 "
    "L-10,26 L-10,20 L-4,20 L-4,14 C-12,12 -20,4 -20,-8 Z "
    "M-22,-24 L-16,-24 L-16,-10 C-20,-12 -22,-18 -22,-24 Z "
    "M22,-24 L16,-24 L16,-10 C20,-12 22,-18 22,-24 Z"
)

# SVG path for a star shape (for S-rank accent), centered at 0,0, radius ~10
_STAR_PATH = (
    "M0,-10 L2.4,-3.1 L9.5,-3.1 L3.8,1.2 L6.2,8.1 "
    "L0,4.5 L-6.2,8.1 L-3.8,1.2 L-9.5,-3.1 L-2.4,-3.1 Z"
)


def _rank_for(trophy: str, value: int) -> str:
    s, a, b = _RANK_THRESHOLDS.get(trophy, (9999, 999, 99))
    if value >= s:
        return "S"
    if value >= a:
        return "A"
    if value >= b:
        return "B"
    return "C"


def _format_value(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(value)


def generate_trophy_case(username: str, theme: str, stats: Optional[dict] = None) -> str:
    """
    Render an 800x200 SVG trophy case with up to 6 trophy cards.

    Args:
        username: GitHub username (displayed in title).
        theme: Theme name key from THEMES dict.
        stats: Optional dict with keys: stars, commits, prs, issues, repos, followers.

    Returns:
        SVG string.
    """
    tokens = _get_theme_tokens(theme)

    bg1 = tokens["bg_gradient"][0]
    bg2 = tokens["bg_gradient"][1]
    accent_color = tokens["accent"]
    text_color = tokens["text"]
    font_header = tokens["font_family_header"]
    font_data = tokens["font_family_data"]

    # Default placeholder stats
    defaults = {
        "stars":     0,
        "commits":   0,
        "prs":       0,
        "issues":    0,
        "repos":     0,
        "followers": 0,
    }
    if stats:
        defaults.update(stats)

    trophies = [
        ("Stars",     defaults["stars"]),
        ("Commits",   defaults["commits"]),
        ("PRs",       defaults["prs"]),
        ("Issues",    defaults["issues"]),
        ("Repos",     defaults["repos"]),
        ("Followers", defaults["followers"]),
    ]

    width, height = 800, 230
    header_h = 36
    card_w, card_h = 120, 170
    padding_x = (width - len(trophies) * card_w) // (len(trophies) + 1)
    start_y = header_h + (height - header_h - card_h) // 2  # vertically center below header

    card_groups = []
    for idx, (name, value) in enumerate(trophies):
        rank = _rank_for(name, value)
        rank_color = _RANK_COLORS[rank] if _RANK_COLORS[rank] else text_color
        cx = padding_x + idx * (card_w + padding_x) + card_w // 2
        cy = start_y

        # S-rank: glow filter + rect pulse animation (animate inside rect)
        glow_filter = ""
        anim_inside_rect = ""
        filter_def_id = f"sglow{idx}"
        if rank == "S":
            glow_filter = f'filter="url(#{filter_def_id})"'
            anim_inside_rect = (
                '\n      <animate attributeName="opacity" '
                'values="0.85;1;0.85" dur="2s" repeatCount="indefinite"/>'
            )

        star_el = ""
        if rank == "S":
            star_el = (
                f'<g transform="translate({card_w // 2},20)" '
                f'fill="{rank_color}" opacity="0.9">'
                f'<path d="{_STAR_PATH}"/></g>'
            )

        card = f"""  <!-- Trophy: {name} (rank {rank}) -->
  <g transform="translate({cx - card_w // 2},{cy})">
    <rect width="{card_w}" height="{card_h}" rx="10" ry="10"
          fill="{bg2}" fill-opacity="0.8"
          stroke="{rank_color}" stroke-width="1.5" {glow_filter}>{anim_inside_rect}
    </rect>
    {star_el}
    <!-- Cup icon -->
    <g transform="translate({card_w // 2},62)" fill="{rank_color}" opacity="0.9">
      <path d="{_TROPHY_CUP_PATH}"/>
    </g>
    <!-- Title -->
    <text x="{card_w // 2}" y="{card_h - 55}" text-anchor="middle"
          font-family="{font_data}" font-size="11" fill="{text_color}">{name}</text>
    <!-- Value -->
    <text x="{card_w // 2}" y="{card_h - 38}" text-anchor="middle"
          font-family="{font_header}" font-size="15" font-weight="bold"
          fill="{rank_color}">{_format_value(value)}</text>
    <!-- Rank badge -->
    <rect x="{card_w // 2 - 13}" y="{card_h - 28}" width="26" height="18" rx="5"
          fill="{rank_color}" opacity="0.18"/>
    <text x="{card_w // 2}" y="{card_h - 14}" text-anchor="middle"
          font-family="{font_header}" font-size="12" font-weight="bold"
          fill="{rank_color}">{rank}</text>
  </g>"""
        card_groups.append(card)

    # Build S-rank filter defs
    filter_defs = []
    for idx, (name, value) in enumerate(trophies):
        rank = _rank_for(name, value)
        if rank == "S":
            rank_color = _RANK_COLORS["S"]
            filter_defs.append(f"""    <filter id="sglow{idx}" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-color="{rank_color}" flood-opacity="0.4" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>""")

    filters_block = "\n".join(filter_defs)
    cards_block = "\n".join(card_groups)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
{filters_block}
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="12"/>

  <!-- Header -->
  <text x="16" y="24" font-family="{font_header}" font-size="12"
        font-weight="bold" fill="{accent_color}" opacity="0.7"
        letter-spacing="1">TROPHY CASE</text>
  <text x="200" y="24" font-family="{font_data}" font-size="11"
        fill="{text_color}" opacity="0.4">@{username}</text>
  <line x1="16" y1="32" x2="784" y2="32" stroke="{accent_color}"
        stroke-width="0.5" opacity="0.2"/>

  <!-- Trophy cards -->
{cards_block}
</svg>"""

    return svg
