from .server import mcp

THEMES = {
    "luxury-glass": {
        "bg_gradient": ["#0b0f14", "#151c25"],
        "accent": "#b6a891",
        "text": "#eceff4",
        "border": "#2b303a",
        "font_family_header": "Segoe UI, Inter, sans-serif",
        "font_family_data": "Consolas, monospace"
    },
    "terminal-hacker": {
        "bg_gradient": ["#000000", "#050705"],
        "accent": "#00ff41",
        "text": "#00b32c",
        "border": "#003300",
        "font_family_header": "Courier New, monospace",
        "font_family_data": "Courier New, monospace"
    },
    "minimalist": {
        "bg_gradient": ["#ffffff", "#f5f7fa"],
        "accent": "#111827",
        "text": "#24292f",
        "border": "#d0d7de",
        "font_family_header": "-apple-system, sans-serif",
        "font_family_data": "SFMono-Regular, monospace"
    },
    "cyberpunk": {
        "bg_gradient": ["#0d0221", "#26043b"],
        "accent": "#ff003c",
        "text": "#00f0ff",
        "border": "#4b0082",
        "font_family_header": "system-ui, sans-serif",
        "font_family_data": "Courier New, monospace"
    }
}

@mcp.resource("theme://{name}")
def get_theme(name: str) -> str:
    """Get the specific CSS hex tokens and typography for a chosen theme engine."""
    import json
    if name in THEMES:
        return json.dumps(THEMES[name], indent=2)
    return '{"error": "Theme not found. Available: luxury-glass, terminal-hacker, minimalist, cyberpunk"}'
