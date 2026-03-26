def _get_theme_tokens(theme_name: str) -> dict:
    from ..resources import THEMES
    return THEMES.get(theme_name, THEMES["luxury-glass"])


def generate_map(tech_stack: dict, theme: str) -> str:
    """
    Generates an 800x260 SVG neural network map with glowing nodes, Bezier edges,
    and animated data-flow particles connecting tech stack categories.

    Args:
        tech_stack: Dict of {category: [tech, ...]} e.g. {"Frontend": ["React", "Next.js"]}
        theme: Theme name from THEMES dict.

    Returns:
        Raw SVG XML string.
    """
    tokens = _get_theme_tokens(theme)
    accent = tokens["accent"]
    text_col = tokens["text"]
    bg1 = tokens["bg_gradient"][0]
    bg2 = tokens["bg_gradient"][1]
    font = tokens["font_family_data"]

    width, height = 800, 260
    categories = list(tech_stack.items())
    n_cols = len(categories)

    # Column x positions spread evenly
    col_xs = [int(width * (i + 1) / (n_cols + 1)) for i in range(n_cols)]

    # Node positions per column
    node_positions = []
    for col_i, (cat, techs) in enumerate(categories):
        cx = col_xs[col_i]
        n = len(techs)
        ys = [int(height * (j + 1) / (n + 1)) for j in range(n)]
        node_positions.append(list(zip([cx] * n, ys, techs)))

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    svg.append('  <defs>')
    svg.append('    <linearGradient id="nbg" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append(f'      <stop offset="0%" stop-color="{bg1}"/>')
    svg.append(f'      <stop offset="100%" stop-color="{bg2}"/>')
    svg.append('    </linearGradient>')

    # Radial gradient for each node glow
    svg.append('    <radialGradient id="nglow" cx="50%" cy="50%" r="50%">')
    svg.append(f'      <stop offset="0%" stop-color="{accent}" stop-opacity="0.9"/>')
    svg.append(f'      <stop offset="60%" stop-color="{accent}" stop-opacity="0.4"/>')
    svg.append(f'      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    # Glow filter
    svg.append('    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">')
    svg.append('      <feGaussianBlur stdDeviation="4" result="blur"/>')
    svg.append('      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')
    svg.append('  </defs>')

    # Background
    svg.append(f'  <rect width="{width}" height="{height}" fill="url(#nbg)" rx="12"/>')

    # Draw Bezier edges between adjacent columns
    edge_paths = []
    for col_i in range(n_cols - 1):
        for (x1, y1, _) in node_positions[col_i]:
            for (x2, y2, _) in node_positions[col_i + 1]:
                cp1x = x1 + (x2 - x1) // 3
                cp2x = x2 - (x2 - x1) // 3
                path = f"M{x1} {y1} C{cp1x} {y1},{cp2x} {y2},{x2} {y2}"
                edge_paths.append(path)
                svg.append(f'  <path d="{path}" fill="none" stroke="{accent}" stroke-width="1" opacity="0.2"/>')

    # Animated particles along each edge
    for i, path in enumerate(edge_paths):
        dur = 2.5 + (i % 3) * 0.7
        svg.append(f'  <circle r="2.5" fill="{accent}" opacity="0.9" filter="url(#glow)">')
        svg.append(f'    <animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/>')
        svg.append('  </circle>')

    # Draw nodes + labels
    for col_i, (cat, techs) in enumerate(categories):
        cx = col_xs[col_i]

        # Category label
        svg.append(f'  <text x="{cx}" y="18" text-anchor="middle" '
                   f'font-family="{font}" font-size="10" fill="{accent}" opacity="0.7"'
                   f' font-weight="bold" letter-spacing="2">{cat.upper()}</text>')

        for (nx, ny, tech) in node_positions[col_i]:
            # Glow halo
            svg.append(f'  <circle cx="{nx}" cy="{ny}" r="22" fill="url(#nglow)" opacity="0.5"/>')
            # Node ring
            svg.append(f'  <circle cx="{nx}" cy="{ny}" r="14" fill="{bg2}" '
                       f'stroke="{accent}" stroke-width="1.5" opacity="0.9"/>')
            # Node core
            svg.append(f'  <circle cx="{nx}" cy="{ny}" r="5" fill="{accent}" filter="url(#glow)"/>')
            # Tech label below node
            svg.append(f'  <text x="{nx}" y="{ny + 28}" text-anchor="middle" '
                       f'font-family="{font}" font-size="11" fill="{text_col}" opacity="0.9">{tech}</text>')

    svg.append('</svg>')
    return "\n".join(svg)
