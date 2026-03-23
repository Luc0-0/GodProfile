import json

def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])

def generate_svg_card(theme: str, title: str, description: str, tags: list[str], identifier: str) -> str:
    """
    Generates a premium 390x150 SVG rendering utilizing the requested aesthetic tokens.
    Automatically injects Python scraping placeholders matching the `{identifier}`.
    
    Args:
        theme: "luxury-glass", "terminal-hacker", "minimalist", or "cyberpunk".
        title: Main project string
        description: Tagline
        tags: Array of technology tags
        identifier: A unique uppercase string indicating the cron scrape hook (e.g. 'SERENITY')
        
    Returns:
        str: The fully formatted SVG XML code.
    """
    tokens = _get_theme_tokens(theme)
    width, height = 390, 150
    rx = 12 if theme == "luxury-glass" else (0 if theme == "terminal-hacker" else 8)
    
    # Generate tags
    tag_elements = []
    current_x = 24
    for tag in tags:
        tag_elements.append(
            f'<rect x="{current_x}" y="{height - 35}" width="{len(tag)*8 + 16}" height="18" rx="4" '
            f'fill="{tokens["bg_gradient"][1]}" stroke="{tokens["border"]}" stroke-width="0.7"/>\n'
            f'    <text x="{current_x + 8}" y="{height - 23}" '
            f'font-family="{tokens["font_family_data"]}" font-size="9" fill="{tokens["accent"]}">{tag}</text>'
        )
        current_x += (len(tag)*8 + 16) + 8

    tag_str = "\n    ".join(tag_elements)

    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{tokens['bg_gradient'][0]}" />
      <stop offset="100%" stop-color="{tokens['bg_gradient'][1]}" />
    </linearGradient>
    <pattern id="grid" width="14" height="14" patternUnits="userSpaceOnUse">
      <path d="M14 0 H0 V14" fill="none" stroke="{tokens['border']}" stroke-width="0.6" opacity="0.3"/>
    </pattern>
  </defs>

  <!-- Base Plates -->
  <rect width="{width}" height="{height}" fill="url(#bg)" rx="{rx}"/>
  <rect width="{width}" height="{height}" fill="url(#grid)" rx="{rx}"/>
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="card-border" rx="{rx}" fill="none" stroke="{tokens['border']}"/>

  <!-- Accent Geometry -->
  <rect x="0" y="25" width="3" height="100" fill="{tokens['accent']}" opacity="0.8" rx="1"/>

  <!-- Typography -->
  <text x="24" y="35" font-family="{tokens['font_family_header']}" font-size="18" font-weight="bold" fill="{tokens['text']}">{title}</text>
  <text x="24" y="55" font-family="{tokens['font_family_data']}" font-size="11" fill="{tokens['accent']}" opacity="0.8">{description}</text>

  <!-- Dynamic Tracker Injection Placeholder -->
  <!-- This comment block will be overwritten synchronously by setup_github_automation hooks -->
  <text x="{width - 30}" y="35" font-family="{tokens['font_family_data']}" font-size="10" fill="{tokens['text']}" opacity="0.6">
    ★ <!-- STARS_COUNT_{identifier} -->
  </text>
  
  <text x="{width - 70}" y="35" font-family="{tokens['font_family_data']}" font-size="10" fill="{tokens['text']}" opacity="0.6">
    ⑂ <!-- FORKS_COUNT_{identifier} -->
  </text>

  <!-- Tech Stack -->
  <g>
    {tag_str}
  </g>
</svg>"""

    return svg_template
