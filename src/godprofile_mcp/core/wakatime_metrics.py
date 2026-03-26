"""
WakaTime Metrics module for GodProfile MCP Toolkit.
Renders a themed SVG horizontal bar chart of weekly coding activity.
No external dependencies beyond urllib.
"""

import json
import urllib.error
import urllib.request


def _get_theme_tokens(theme_name: str) -> dict:
    try:
        from ..resources import THEMES
        return THEMES.get(theme_name, THEMES["luxury-glass"])
    except Exception:
        return {
            "bg_gradient": ["#0d1117", "#161b22"],
            "accent": "#58a6ff",
            "text": "#c9d1d9",
            "border": "#30363d",
            "font_family_header": "Inter, sans-serif",
            "font_family_data": "JetBrains Mono, monospace",
        }


_PLACEHOLDER_DATA = {
    "Python": 45.2,
    "TypeScript": 30.1,
    "Rust": 15.5,
    "Other": 9.2,
}

# Bar color palette: accent + opacity steps cycling for each language
_BAR_OPACITIES = [1.0, 0.78, 0.58, 0.42, 0.30, 0.22]


def render_wakatime_activity_chart(theme: str, data: dict) -> str:
    """
    Renders a 400x220 SVG horizontal bar chart of WakaTime weekly coding activity.

    Args:
        theme: GodProfile theme name.
        data: Dict of {language: percentage} e.g. {"Python": 45.2, "TypeScript": 30.1}.
              If empty or None, placeholder data is used.

    Returns:
        SVG string.
    """
    tokens = _get_theme_tokens(theme)
    bg1 = tokens["bg_gradient"][0]
    bg2 = tokens["bg_gradient"][1] if len(tokens["bg_gradient"]) > 1 else tokens["bg_gradient"][0]
    accent = tokens["accent"]
    text_color = tokens["text"]
    border_color = tokens["border"]
    font = tokens["font_family_header"]
    mono = tokens["font_family_data"]

    chart_data = data if data else _PLACEHOLDER_DATA

    # Sort descending by percentage, cap to 6 entries
    sorted_items = sorted(chart_data.items(), key=lambda x: x[1], reverse=True)[:6]

    # Layout constants
    width = 400
    bar_area_left = 100   # label column width
    bar_area_right = 340  # bar end boundary
    bar_max_width = bar_area_right - bar_area_left  # 240px
    row_height = 28
    chart_top = 44        # below title
    label_max_chars = 13

    rows_svg = []
    for i, (lang, pct) in enumerate(sorted_items):
        y = chart_top + i * row_height
        bar_w = max(4, int((pct / 100.0) * bar_max_width))
        opacity = _BAR_OPACITIES[i % len(_BAR_OPACITIES)]
        label = lang[:label_max_chars] + ("." if len(lang) > label_max_chars else "")
        pct_str = "{:.1f}%".format(pct)

        # Background track
        rows_svg.append(
            '<rect x="{lx}" y="{ty}" width="{tw}" height="14" rx="4" fill="{bc}" opacity="0.18"/>'.format(
                lx=bar_area_left, ty=y, tw=bar_max_width, bc=border_color
            )
        )
        # Animated bar
        rows_svg.append(
            '<rect x="{lx}" y="{ty}" width="0" height="14" rx="4" fill="{ac}" opacity="{op}">'
            '<animate attributeName="width" from="0" to="{bw}" dur="0.8s" begin="{delay}s" fill="freeze"/>'
            '</rect>'.format(
                lx=bar_area_left, ty=y, ac=accent, op=opacity,
                bw=bar_w, delay=round(0.1 + i * 0.12, 2)
            )
        )
        # Language label
        rows_svg.append(
            '<text x="{lx}" y="{ty}" font-family="{font}" font-size="10" fill="{tc}" text-anchor="end">{label}</text>'.format(
                lx=bar_area_left - 6, ty=y + 11, font=font, tc=text_color, label=label
            )
        )
        # Percentage text
        rows_svg.append(
            '<text x="{px}" y="{ty}" font-family="{mono}" font-size="9" fill="{ac}" opacity="0.85">{pct}</text>'.format(
                px=bar_area_left + bar_w + 5, ty=y + 11, mono=mono, ac=accent, pct=pct_str
            )
        )

    chart_height = chart_top + len(sorted_items) * row_height + 18
    rows_block = "\n  ".join(rows_svg)

    svg = (
        '<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">\n'
        "  <defs>\n"
        '    <linearGradient id="wkBg" x1="0" y1="0" x2="0" y2="1">\n'
        '      <stop offset="0%" stop-color="{bg1}"/>\n'
        '      <stop offset="100%" stop-color="{bg2}"/>\n'
        "    </linearGradient>\n"
        "  </defs>\n"
        '  <rect width="{w}" height="{h}" rx="12" fill="url(#wkBg)" stroke="{bc}" stroke-width="1"/>\n'
        '  <text x="16" y="24" font-family="{font}" font-size="13" font-weight="700" fill="{tc}">WakaTime \u2014 Weekly Coding Activity</text>\n'
        '  <line x1="16" y1="32" x2="{lw}" y2="32" stroke="{ac}" stroke-width="1" opacity="0.3"/>\n'
        "  {rows}\n"
        "</svg>"
    ).format(
        w=width,
        h=chart_height,
        bg1=bg1,
        bg2=bg2,
        bc=border_color,
        font=font,
        tc=text_color,
        ac=accent,
        lw=width - 16,
        rows=rows_block,
    )

    return svg


def fetch_wakatime_stats(api_key: str, theme: str = "luxury-glass") -> str:
    """
    Fetches the last 7 days of coding stats from the WakaTime API and returns
    an SVG chart via render_wakatime_activity_chart().

    Uses urllib only (no external dependencies).
    Falls back to an error SVG card on any failure.

    Args:
        api_key: WakaTime API key (v1).
        theme: GodProfile theme name.

    Returns:
        SVG string.
    """
    import base64

    url = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
    encoded_key = base64.b64encode(api_key.encode()).decode()
    req = urllib.request.Request(
        url,
        headers={"Authorization": "Basic " + encoded_key},
    )

    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw)

        languages_raw = (payload.get("data") or {}).get("languages") or []

        lang_data = {}
        for entry in languages_raw:
            name = entry.get("name") or "Other"
            pct = entry.get("percent")
            if pct is not None:
                try:
                    lang_data[name] = float(pct)
                except (TypeError, ValueError):
                    pass

        if not lang_data:
            return render_wakatime_activity_chart(theme=theme, data={})

        return render_wakatime_activity_chart(theme=theme, data=lang_data)

    except urllib.error.HTTPError as e:
        return _error_card(theme, "WakaTime API Error", "HTTP {}".format(e.code))

    except urllib.error.URLError:
        return _error_card(theme, "Network Error", "Could not reach WakaTime")

    except (json.JSONDecodeError, KeyError, TypeError):
        return _error_card(theme, "Parse Error", "Unexpected API response")


def _error_card(theme: str, title: str, subtitle: str) -> str:
    """Returns a minimal 400x80 SVG error card using theme tokens."""
    tokens = _get_theme_tokens(theme)
    bg1 = tokens["bg_gradient"][0]
    bg2 = tokens["bg_gradient"][1] if len(tokens["bg_gradient"]) > 1 else tokens["bg_gradient"][0]
    text_color = tokens["text"]
    border_color = tokens["border"]
    font = tokens["font_family_header"]

    return (
        '<svg width="400" height="80" xmlns="http://www.w3.org/2000/svg">'
        "<defs>"
        '<linearGradient id="ecBg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0%" stop-color="{bg1}"/>'
        '<stop offset="100%" stop-color="{bg2}"/>'
        "</linearGradient>"
        "</defs>"
        '<rect width="400" height="80" rx="12" fill="url(#ecBg)" stroke="{bc}" stroke-width="1"/>'
        '<text x="20" y="32" font-family="{font}" font-size="13" font-weight="700" fill="{tc}">{title}</text>'
        '<text x="20" y="52" font-family="{font}" font-size="11" fill="{tc}" opacity="0.55">{subtitle}</text>'
        "</svg>"
    ).format(
        bg1=bg1, bg2=bg2, bc=border_color, font=font, tc=text_color,
        title=title, subtitle=subtitle
    )
