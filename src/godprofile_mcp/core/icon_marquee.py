"""
icon_marquee.py — Build an animated SVG icon/tech-badge marquee strip.
stdlib only, no external dependencies.
"""

from html import escape


def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


# Pill geometry
_PILL_H = 28
_PILL_PADDING_X = 14
_PILL_GAP = 10
_FONT_SIZE = 12
_STRIP_Y = (60 - _PILL_H) // 2  # vertical centre inside 60px height


def _estimate_text_width(text: str, font_size: int = _FONT_SIZE) -> int:
    """Rough monospace-style width estimate (good enough for layout)."""
    return len(text) * int(font_size * 0.62)


def _pill_width(label: str) -> int:
    return _estimate_text_width(label) + _PILL_PADDING_X * 2


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert #rrggbb to rgba(r,g,b,alpha)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _render_pill_group(icons: list, tokens: dict, x_offset: int) -> tuple:
    """
    Render a row of pills starting at x_offset.
    Returns (svg_fragment, total_width).
    """
    accent = tokens.get("accent", "#c9a84c")
    text_color = tokens.get("text", "#e0e0e0")
    font_data = tokens.get("font_family_data", "monospace")

    pill_bg = _hex_to_rgba(accent, 0.15)
    pill_stroke = _hex_to_rgba(accent, 0.45)

    parts = []
    x = x_offset
    for label in icons:
        pw = _pill_width(label)
        ph = _PILL_H
        py = _STRIP_Y
        text_x = x + pw // 2
        text_y = py + ph // 2 + _FONT_SIZE // 2 - 1

        parts.append(
            f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="{ph // 2}" '
            f'fill="{pill_bg}" stroke="{pill_stroke}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{text_x}" y="{text_y}" '
            f'font-family="{font_data}" font-size="{_FONT_SIZE}" '
            f'fill="{text_color}" text-anchor="middle" dominant-baseline="auto" '
            f'font-weight="500">{escape(label)}</text>'
        )
        x += pw + _PILL_GAP

    total_width = x - x_offset - _PILL_GAP  # remove trailing gap
    return "\n".join(parts), total_width


def build_marquee(icons: list, theme: str, speed: int = 30) -> str:
    """
    Build an 800x60 SVG with an infinitely scrolling pill/badge marquee.

    icons : list of tech name strings (e.g. ["Python", "React", "Docker"])
    theme : theme name from THEMES dict
    speed : animation duration in seconds (lower = faster scroll)
    """
    tokens = _get_theme_tokens(theme)
    bg1, bg2 = tokens.get("bg_gradient", ["#0d0d0d", "#1a1a2e"])
    border = tokens.get("border", "#333")

    W, H = 800, 60
    grad_id = "mqBg"

    # Compute single-row width
    single_width = sum(_pill_width(ic) + _PILL_GAP for ic in icons)
    # Ensure the duplicated row covers at least the viewport width
    repeat = max(2, -(-W // single_width) + 1)  # ceil div + 1 extra copy
    icons_repeated = icons * repeat

    # First group starts at 0, second group (for seamless loop) starts at single_width
    group1, row_width = _render_pill_group(icons_repeated, tokens, 0)
    # For seamless loop we only need two copies: 0..single_width and single_width..2*single_width
    group2, _ = _render_pill_group(icons * 2, tokens, single_width)

    # Animation: translate from 0 to -single_width (one full cycle = seamless)
    anim_duration = max(1, speed)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack marquee">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <clipPath id="mqClip">
      <rect width="{W}" height="{H}" rx="10"/>
    </clipPath>
    <style>
      @keyframes mqScroll {{
        0%   {{ transform: translateX(0px); }}
        100% {{ transform: translateX(-{single_width}px); }}
      }}
      .mq-track {{
        animation: mqScroll {anim_duration}s linear infinite;
        will-change: transform;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="10" fill="url(#{grad_id})"/>
  <rect width="{W}" height="{H}" rx="10" fill="none"
        stroke="{border}" stroke-width="1" opacity="0.5"/>

  <!-- Scrolling track (clipped) -->
  <g clip-path="url(#mqClip)">
    <g class="mq-track">
      {group1}
      {group2}
    </g>
  </g>
</svg>"""
    return svg
