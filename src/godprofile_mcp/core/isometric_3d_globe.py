"""Isometric 3D globe SVG generator using stdlib + math only."""

import math
from typing import Optional


def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


def _iso_project(x: float, y: float, z: float) -> tuple:
    """Apply isometric projection with 30-degree angles."""
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    sx = (x - z) * cos30
    sy = y + (x + z) * sin30
    return sx, sy


def _sphere_point(phi: float, theta: float) -> tuple:
    """Parametric unit sphere: (sin(phi)*cos(theta), cos(phi), sin(phi)*sin(theta))."""
    x = math.sin(phi) * math.cos(theta)
    y = math.cos(phi)
    z = math.sin(phi) * math.sin(theta)
    return x, y, z


def generate_globe(theme: str = "luxury-glass", highlight_points: Optional[list] = None) -> str:
    """
    Render a 400x400 SVG isometric globe with lat/lon grid lines and animated rotation.

    Args:
        theme: Theme name key from THEMES dict.
        highlight_points: List of [lat, lon] pairs (degrees) to mark with dots.

    Returns:
        SVG string.
    """
    tokens = _get_theme_tokens(theme)
    if highlight_points is None:
        highlight_points = []

    bg1 = tokens["bg_gradient"][0]
    bg2 = tokens["bg_gradient"][1]
    border_color = tokens["border"]
    accent_color = tokens["accent"]
    text_color = tokens["text"]
    font_data = tokens["font_family_data"]

    width, height = 400, 400
    cx, cy = 200, 200
    scale = 100  # sphere radius in SVG units

    # --- Longitude lines (12 lines, every 30 degrees) ---
    lon_path_els = []
    for i in range(12):
        theta = math.radians(i * 30)
        pts = []
        for j in range(61):
            phi = math.radians(j * 3)  # 0..180
            x, y, z = _sphere_point(phi, theta)
            sx, sy = _iso_project(x, y, z)
            pts.append(f"{cx + sx * scale:.2f},{cy - sy * scale:.2f}")
        d = "M " + " L ".join(pts)
        lon_path_els.append(
            f'<path d="{d}" fill="none" stroke="{border_color}" stroke-width="0.8" opacity="0.55"/>'
        )

    # --- Latitude lines (8 lines, evenly spaced, skipping poles) ---
    lat_path_els = []
    for i in range(1, 9):
        phi = math.radians(i * 20)  # 20,40,...,160
        pts = []
        for j in range(73):
            theta = math.radians(j * 5)  # 0..360
            x, y, z = _sphere_point(phi, theta)
            sx, sy = _iso_project(x, y, z)
            pts.append(f"{cx + sx * scale:.2f},{cy - sy * scale:.2f}")
        d = "M " + " L ".join(pts)
        lat_path_els.append(
            f'<path d="{d}" fill="none" stroke="{border_color}" stroke-width="0.8" opacity="0.55"/>'
        )

    # --- Highlight dot markers ---
    dot_els = []
    for point in highlight_points:
        if len(point) >= 2:
            lat_deg, lon_deg = float(point[0]), float(point[1])
            phi = math.radians(90.0 - lat_deg)
            theta = math.radians(lon_deg)
            x, y, z = _sphere_point(phi, theta)
            sx, sy = _iso_project(x, y, z)
            px = cx + sx * scale
            py = cy - sy * scale
            dot_els.append(
                f'<circle cx="{px:.2f}" cy="{py:.2f}" r="4" fill="{accent_color}" '
                f'stroke="{text_color}" stroke-width="1" opacity="0.9"/>'
            )

    lon_block = "\n      ".join(lon_path_els)
    lat_block = "\n      ".join(lat_path_els)
    dot_block = "\n      ".join(dot_els)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{bg1}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </radialGradient>
    <radialGradient id="globeGrad" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{bg1}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{bg2}" stop-opacity="0.92"/>
    </radialGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="globeClip">
      <circle cx="{cx}" cy="{cy}" r="{scale}"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="12"/>

  <!-- Rotating globe group -->
  <g id="globe-group">
    <!-- Globe fill -->
    <circle cx="{cx}" cy="{cy}" r="{scale}" fill="url(#globeGrad)"
            stroke="{border_color}" stroke-width="1.5" filter="url(#glow)"/>

    <!-- Grid lines clipped to sphere -->
    <g clip-path="url(#globeClip)">
      {lon_block}
      {lat_block}
      {dot_block}
    </g>

    <!-- Accent ring -->
    <circle cx="{cx}" cy="{cy}" r="{scale}" fill="none"
            stroke="{accent_color}" stroke-width="1.5" opacity="0.25"/>

    <!-- Animated Y-axis rotation (visual sweep via transform rotate) -->
    <animateTransform attributeName="transform" attributeType="XML"
      type="rotate"
      from="0 {cx} {cy}"
      to="360 {cx} {cy}"
      dur="30s"
      repeatCount="indefinite"/>
  </g>

  <!-- Label -->
  <text x="{cx}" y="{height - 16}" text-anchor="middle"
        font-family="{font_data}" font-size="11"
        fill="{text_color}" opacity="0.55">GodProfile Globe</text>
</svg>"""

    return svg
