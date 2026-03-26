import os


def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


def capture_banner_gif(theme: str, lines: list, path: str) -> str:
    """
    Creates an 800x200 animated SVG banner with sequential fade-in text lines,
    gradient background, and floating particle dots.

    Args:
        theme: theme name string
        lines: list of text strings to display
        path: optional file path to save the SVG

    Returns:
        SVG string
    """
    tokens = _get_theme_tokens(theme)
    bg1, bg2 = tokens.get("bg_gradient", ["#0d1117", "#161b22"])
    accent = tokens.get("accent", "#58a6ff")
    text_color = tokens.get("text", "#c9d1d9")
    font_header = tokens.get("font_family_header", "sans-serif")

    width = 800
    height = 200
    delay_per_line = 0.6

    # Particle definitions (8 subtle dots floating upward)
    particle_data = [
        (120, 160, 3, 4.0, 0.0),
        (250, 180, 2, 6.0, 1.2),
        (400, 170, 4, 5.0, 0.5),
        (530, 150, 2, 7.0, 2.1),
        (660, 175, 3, 4.5, 1.7),
        (740, 140, 2, 6.5, 0.3),
        (80,  130, 3, 5.5, 2.8),
        (320, 190, 2, 4.8, 1.0),
    ]

    particle_css_parts = []
    particle_elements = []
    for idx, (px, py, pr, dur, delay) in enumerate(particle_data):
        pid = f"p{idx}"
        particle_css_parts.append(
            f".{pid} {{ animation: float {dur:.1f}s {delay:.1f}s ease-in-out infinite alternate; opacity: 0.25; }}"
        )
        particle_elements.append(
            f'  <circle cx="{px}" cy="{py}" r="{pr}" fill="{accent}" class="{pid}"/>'
        )

    particle_css = "\n    ".join(particle_css_parts)
    particles_block = "\n".join(particle_elements)

    # Text line CSS
    line_css_parts = []
    for i in range(len(lines)):
        delay = i * delay_per_line
        line_css_parts.append(
            f".l{i} {{ opacity: 0; animation: fadein 0.7s {delay:.2f}s ease forwards; }}"
        )
    line_css = "\n    ".join(line_css_parts)

    full_css = f"""
    @keyframes fadein {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes float {{ from {{ transform: translateY(0px); }} to {{ transform: translateY(-12px); }} }}
    {particle_css}
    {line_css}
    """

    # Distribute lines vertically
    n = len(lines)
    line_elements = []
    for i, line in enumerate(lines):
        y = int(height * (i + 1) / (n + 1))
        safe = (
            line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
        )
        line_elements.append(
            f'  <text x="{width // 2}" y="{y}" text-anchor="middle" dominant-baseline="middle" '
            f'fill="{text_color}" font-family="{font_header}, sans-serif" '
            f'font-size="22" font-weight="bold" class="l{i}">{safe}</text>'
        )
    lines_block = "\n".join(line_elements)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <style>
    {full_css}
    </style>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bg-grad)" rx="10" ry="10"/>

  <!-- Particles -->
{particles_block}

  <!-- Text lines -->
{lines_block}
</svg>'''

    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)

    return svg


def generate_banner(title: str, subtitle: str, theme: str) -> str:
    """
    Creates an 800x160 SVG project banner with a geometric logo, title, subtitle,
    accent underline, and fade-in animation. Designed for README headers.

    Args:
        title: main heading text
        subtitle: secondary text below the title
        theme: theme name string

    Returns:
        SVG string
    """
    tokens = _get_theme_tokens(theme)
    bg1, bg2 = tokens.get("bg_gradient", ["#0d1117", "#161b22"])
    accent = tokens.get("accent", "#58a6ff")
    text_color = tokens.get("text", "#c9d1d9")
    font_header = tokens.get("font_family_header", "sans-serif")
    font_data = tokens.get("font_family_data", "monospace")

    width, height = 800, 160
    cx, cy = 80, 80  # logo center

    # Geometric logo: central node + 6 orbital nodes connected by lines
    orbital_r = 28
    node_angles = [0, 60, 120, 180, 240, 300]
    import math
    orbitals = [
        (cx + orbital_r * math.cos(math.radians(a)),
         cy + orbital_r * math.sin(math.radians(a)))
        for a in node_angles
    ]

    # Build spoke lines and orbital dots
    spokes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{ox:.1f}" y2="{oy:.1f}" '
        f'stroke="{accent}" stroke-width="1" opacity="0.35"/>'
        for ox, oy in orbitals
    )
    orbit_dots = "".join(
        f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="3" fill="{accent}" opacity="0.6"/>'
        for ox, oy in orbitals
    )

    safe_title = (
        title.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;")
    )
    safe_subtitle = (
        subtitle.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;")
    )

    # Underline width based on title length
    underline_w = min(len(title) * 14, 320)
    text_x = 130

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <radialGradient id="logo-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <style>
    @keyframes fadein {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} }}
    .title    {{ opacity: 0; animation: fadein 0.8s 0.2s ease forwards; }}
    .subtitle {{ opacity: 0; animation: fadein 0.8s 0.7s ease forwards; }}
    .uline    {{ opacity: 0; animation: fadein 0.5s 1.1s ease forwards; }}
    .logo-core {{ animation: pulse 2.5s ease-in-out infinite; }}
    </style>
  </defs>

  <rect width="{width}" height="{height}" fill="url(#bg-grad)" rx="10"/>

  <!-- Logo glow halo -->
  <circle cx="{cx}" cy="{cy}" r="48" fill="url(#logo-glow)"/>
  <!-- Logo orbit ring -->
  <circle cx="{cx}" cy="{cy}" r="{orbital_r}" fill="none" stroke="{accent}" stroke-width="0.75" opacity="0.2"/>
  <!-- Logo spokes -->
  {spokes}
  <!-- Logo orbital dots -->
  {orbit_dots}
  <!-- Logo core node -->
  <circle cx="{cx}" cy="{cy}" r="7" fill="{accent}" class="logo-core"/>
  <circle cx="{cx}" cy="{cy}" r="3" fill="{bg1}"/>

  <!-- Title -->
  <text x="{text_x}" y="66" dominant-baseline="middle"
        fill="{text_color}" font-family="{font_header}"
        font-size="38" font-weight="bold" class="title">{safe_title}</text>

  <!-- Accent underline -->
  <rect x="{text_x}" y="84" width="{underline_w}" height="2.5" fill="{accent}" rx="1.5" class="uline"/>

  <!-- Subtitle -->
  <text x="{text_x}" y="112" dominant-baseline="middle"
        fill="{accent}" font-family="{font_data}"
        font-size="14" opacity="0.8" class="subtitle">{safe_subtitle}</text>
</svg>'''

    return svg
