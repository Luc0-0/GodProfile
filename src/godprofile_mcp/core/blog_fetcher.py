"""
blog_fetcher.py — Fetch RSS/Atom feeds and render themed SVG cards.
stdlib only: urllib, xml.etree.ElementTree
"""

import xml.etree.ElementTree as ET
from html import escape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


def _build_rss_url(provider: str, username: str) -> str:
    p = provider.lower().strip()
    if p == "devto":
        return f"https://dev.to/feed/{username}"
    elif p == "medium":
        return f"https://medium.com/feed/@{username}"
    elif p == "hashnode":
        return f"https://{username}.hashnode.dev/rss.xml"
    else:
        # treat provider as a direct URL
        return provider


def _fetch_xml(url: str, timeout: int = 5) -> ET.Element:
    req = Request(url, headers={"User-Agent": "GodProfile-MCP/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return ET.fromstring(data)


def _parse_items(root: ET.Element) -> list:
    """Extract up to 5 items from RSS or Atom feed."""
    ns_atom = "http://www.w3.org/2005/Atom"
    items = []

    # RSS 2.0
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item")[:5]:
            title = (item.findtext("title") or "Untitled").strip()
            link = (item.findtext("link") or "#").strip()
            pub_date = (item.findtext("pubDate") or "")[:16].strip()
            items.append((title, pub_date, link))
        return items

    # Atom
    for entry in root.findall(f"{{{ns_atom}}}entry")[:5]:
        title = (entry.findtext(f"{{{ns_atom}}}title") or "Untitled").strip()
        pub_date = (entry.findtext(f"{{{ns_atom}}}published") or "")[:10].strip()
        link_el = entry.find(f"{{{ns_atom}}}link")
        link = (link_el.get("href") if link_el is not None else "#") or "#"
        items.append((title, pub_date, link))

    return items


def _truncate(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[:max_len - 1] + "…"


def _render_svg(items: list, theme_tokens: dict, header: str = "Latest Posts") -> str:
    bg1, bg2 = theme_tokens.get("bg_gradient", ["#0d0d0d", "#1a1a2e"])
    accent = theme_tokens.get("accent", "#c9a84c")
    text_color = theme_tokens.get("text", "#e0e0e0")
    border = theme_tokens.get("border", "#333")
    font_header = theme_tokens.get("font_family_header", "Georgia, serif")
    font_data = theme_tokens.get("font_family_data", "monospace")

    W, H = 400, 280
    row_h = 38
    list_top = 56
    grad_id = "blogBg"

    rows_svg = []
    for i, (title, pub_date, link) in enumerate(items):
        y = list_top + i * row_h
        display_title = escape(_truncate(title, 44))
        display_date = escape(pub_date[:10]) if pub_date else ""
        row_bg = "rgba(255,255,255,0.04)" if i % 2 == 0 else "rgba(0,0,0,0.0)"
        rows_svg.append(f"""
    <rect x="16" y="{y}" width="{W - 32}" height="{row_h - 4}" rx="4"
          fill="{row_bg}" />
    <a href="{escape(link)}" target="_blank">
      <text x="24" y="{y + 16}" font-family="{font_data}" font-size="12"
            fill="{text_color}" font-weight="500">{display_title}</text>
      <text x="24" y="{y + 30}" font-family="{font_data}" font-size="10"
            fill="{accent}" opacity="0.8">{display_date}</text>
    </a>""")

    rows_block = "".join(rows_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="{escape(header)}">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="12" fill="url(#{grad_id})"/>
  <rect width="{W}" height="{H}" rx="12" fill="none"
        stroke="{border}" stroke-width="1.5" opacity="0.6"/>

  <!-- Header bar -->
  <rect x="0" y="0" width="{W}" height="44" rx="12" fill="{accent}" opacity="0.15"/>
  <rect x="0" y="32" width="{W}" height="12" fill="{accent}" opacity="0.15"/>
  <line x1="16" y1="44" x2="{W - 16}" y2="44" stroke="{accent}"
        stroke-width="1" opacity="0.4"/>

  <!-- Accent dot -->
  <circle cx="24" cy="22" r="5" fill="{accent}" opacity="0.9"/>

  <!-- Header text -->
  <text x="38" y="28" font-family="{font_header}" font-size="15"
        font-weight="700" fill="{text_color}" letter-spacing="0.5">{escape(header)}</text>

  <!-- Posts -->
  {rows_block}
</svg>"""
    return svg


def _error_svg(message: str, theme_tokens: dict) -> str:
    bg1, bg2 = theme_tokens.get("bg_gradient", ["#0d0d0d", "#1a1a2e"])
    accent = theme_tokens.get("accent", "#c9a84c")
    text_color = theme_tokens.get("text", "#e0e0e0")
    border = theme_tokens.get("border", "#333")
    font_data = theme_tokens.get("font_family_data", "monospace")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280"
     viewBox="0 0 400 280" role="img" aria-label="Error">
  <defs>
    <linearGradient id="errBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
  </defs>
  <rect width="400" height="280" rx="12" fill="url(#errBg)"/>
  <rect width="400" height="280" rx="12" fill="none"
        stroke="{border}" stroke-width="1.5" opacity="0.6"/>
  <text x="200" y="130" font-family="{font_data}" font-size="13"
        fill="{accent}" text-anchor="middle">Could not load posts</text>
  <text x="200" y="154" font-family="{font_data}" font-size="10"
        fill="{text_color}" text-anchor="middle" opacity="0.6">{escape(message[:60])}</text>
</svg>"""


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_articles(provider: str, username: str, theme: str) -> str:
    """
    Fetch up to 5 latest posts from a blog provider and return a themed SVG card.

    provider: "devto" | "medium" | "hashnode" | direct RSS URL
    username: author handle (ignored when provider is a direct URL)
    theme:    theme name from THEMES dict
    """
    tokens = _get_theme_tokens(theme)
    url = _build_rss_url(provider, username)
    try:
        root = _fetch_xml(url)
        items = _parse_items(root)
        if not items:
            return _error_svg("No posts found in feed.", tokens)
        provider_label = provider if provider.startswith("http") else provider.title()
        header = f"{provider_label} — {username}"
        return _render_svg(items, tokens, header=header)
    except (HTTPError, URLError) as exc:
        return _error_svg(str(exc), tokens)
    except ET.ParseError as exc:
        return _error_svg(f"XML parse error: {exc}", tokens)
    except Exception as exc:
        return _error_svg(str(exc), tokens)


def fetch_blog_posts(rss_url: str, theme: str = "luxury-glass") -> str:
    """
    Directly fetch any RSS/Atom URL and return a themed SVG card.
    """
    tokens = _get_theme_tokens(theme)
    try:
        root = _fetch_xml(rss_url)
        items = _parse_items(root)
        if not items:
            return _error_svg("No posts found in feed.", tokens)
        return _render_svg(items, tokens, header="Latest Posts")
    except (HTTPError, URLError) as exc:
        return _error_svg(str(exc), tokens)
    except ET.ParseError as exc:
        return _error_svg(f"XML parse error: {exc}", tokens)
    except Exception as exc:
        return _error_svg(str(exc), tokens)
